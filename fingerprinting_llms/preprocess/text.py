import logging
import re
from dataclasses import dataclass

import ftfy
import regex as rxx
from rapidfuzz.distance import Levenshtein
from wordfreq import zipf_frequency

# Optional: spaCy only if you enable NER/entity masking or sentence-aware ops
try:
    import spacy

    _NLP = spacy.load("en_core_web_sm")
except Exception:
    _NLP = None

# -----------------------------------------------------------------------------
# Logging setup
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
@dataclass
class TextPreprocessorConfig:
    """
    Configuration flags for the text cleaning pipeline.

    Parameters
    ----------
    strip_reuters_scaffolding : bool
        If True, remove wire-service artifacts (datelines, bylines, credits,
        prefix tags like UPDATE/EXCLUSIVE). Default **False** to avoid
        altering dataset-specific metadata unless explicitly requested.
    normalize_unicode : bool
        If True, normalize Unicode using ftfy, convert curly quotes to straight
        quotes, normalize dashes to '-', and replace NBSP with space.
    normalize_spacing_punct : bool
        If True, enforce spacing rules around punctuation, collapse multiple
        spaces/newlines, and reduce repeated ?/! to a single mark.
    fix_linebreak_hyphenation : bool
        If True, de-hyphenate words broken across line breaks and unwrap
        single newlines inside paragraphs.
    normalize_dates_times : bool
        If True, normalize common date patterns to YYYY-MM-DD and common times
        to 24h HH:MM, and fix common %/$ spacing issues.
    entity_masking : bool
        If True, replace recognized entities with <LABEL_i> tags (requires spaCy).
        Keep False for your primary run; use as a separate experiment.

    conservative_spelling : bool
        If True, apply a very conservative spelling correction that fixes only
        obvious repeated-letter typos when a very common alternative exists.
    max_change_ratio : float
        Max fraction of alpha tokens per document that may be altered by the
        spelling corrector. If exceeded, the spell pass is **aborted**.
    min_zipf_for_correction : float
        Only correct to candidates with wordfreq.zipf_frequency >= this value,
        i.e., to fairly common English words.

    english_only : bool
        Placeholder for a language ID step (not implemented below). Keep True
        if you plan to plug in a langid check later.
    dedupe_signature : bool
        Placeholder toggle for emitting a signature for dedupe (not used inside
        clean_document; provided for pipeline completeness).
    """

    strip_reuters_scaffolding: bool = False
    normalize_unicode: bool = True
    normalize_spacing_punct: bool = True
    fix_linebreak_hyphenation: bool = True
    normalize_dates_times: bool = True
    entity_masking: bool = False
    #   These 3 are for spelling
    conservative_spelling: bool = False
    max_change_ratio: float = 0.01
    min_zipf_for_correction: float = 4.0
    #   Not implemented
    english_only: bool = False
    dedupe_signature: bool = False


# -----------------------------------------------------------------------------
# Regexes & helpers
# -----------------------------------------------------------------------------
DATELINE_RE = re.compile(r"^(?:[A-Z][A-Z\s\-\.]+)\s*\((?:Reuters|REUTERS)\)\s*[-—]\s*", re.M)
BYLINE_RE = re.compile(r"^\s*(?:By\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*$", re.M)
CREDIT_RE = re.compile(r"\(Reporting by [^)]+(?:; Editing by [^)]+)?\)\s*$", re.M)
COPY_RE = re.compile(r"©?\s*Reuters[^\n]*$", re.M)
WIRE_PREFIX_RE = re.compile(
    r"^(?:UPDATE\s*\d+|EXCLUSIVE|ANALYSIS|FACTBOX|TIMELINE)\s*[-:]\s*", re.M
)

MONTHS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "sept": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}
DATE_PATTERNS = [
    # September 29, 2025
    (
        re.compile(r"\b(" + "|".join(MONTHS.keys()) + r")\.?\s+(\d{1,2}),\s*(\d{4})", re.I),
        lambda m: f"{m.group(3)}-{MONTHS[m.group(1).lower()]}-{int(m.group(2)):02d}",
    ),
    # 29 September 2025
    (
        re.compile(r"\b(\d{1,2})\s+(" + "|".join(MONTHS.keys()) + r")\.?\s+(\d{4})", re.I),
        lambda m: f"{m.group(3)}-{MONTHS[m.group(2).lower()]}-{int(m.group(1)):02d}",
    ),
]
TIME_REPLACERS = [
    # 3:05 pm → 15:05
    (
        re.compile(r"\b(\d{1,2}):(\d{2})\s*(am|pm)\b", re.I),
        lambda m: f"{int(m.group(1)) % 12 + (12 if m.group(3).lower()=='pm' else 0):02d}:{m.group(2)}",
    ),
]

_WORD_RE = re.compile(r"[A-Za-z]([A-Za-z\-']*[A-Za-z])?")  # words ≥2 letters


# -----------------------------------------------------------------------------
# Cleaning functions (each logs change counts)
# -----------------------------------------------------------------------------
def normalize_unicode(text: str) -> str:
    """
    Normalize Unicode artifacts and harmonize punctuation.

    - Fixes mojibake via ftfy.
    - Replaces NBSP with space.
    - Converts curly quotes to straight quotes.
    - Normalizes en/em dashes to hyphen.

    Logs:
      * Count of quote replacements, dash replacements, NBSP replacements,
        and whether ftfy altered the string.
    """
    before = text
    # Count occurrences before replacing (so we can log deltas)
    nbsp_count = text.count("\u00a0")
    quotes_count = sum(text.count(ch) for ch in ["“", "”", "‘", "’"])
    dash_count = sum(text.count(ch) for ch in ["—", "–"])

    text_fixed = ftfy.fix_text(text)
    ftfy_changed = text_fixed != text
    text = text_fixed.replace("\u00a0", " ")
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    text = text.replace("—", "-").replace("–", "-")

    logger.info(
        "normalize_unicode: ftfy_changed=%s, nbsp=%d, curly_quotes=%d, long_dashes=%d",
        ftfy_changed,
        nbsp_count,
        quotes_count,
        dash_count,
    )
    return text


def normalize_spacing_and_punct(text: str) -> str:
    """
    Enforce conservative spacing rules around punctuation and tidy whitespace.

    Rules:
      - Remove spaces before , . ; : ? !
      - Ensure one space after sentence enders if followed by a letter/quote
      - Collapse multiple spaces
      - Reduce repeated ? or ! to a single character
      - Normalize 3+ newlines down to two (paragraph boundary)

    Logs:
      * Counts for each sub-transformation applied.
    """
    counts = {}

    def sub_count(pattern, repl, s, flags=0):
        new_s, n = re.subn(pattern, repl, s, flags=flags)
        return new_s, n

    s = text
    s, n1 = sub_count(r"\s+([,.;:?!])", r"\1", s)
    counts["spaces_before_punct"] = n1

    s, n2 = sub_count(r'([.?!])([A-Za-z"])', r"\1 \2", s)
    counts["missing_space_after_ender"] = n2

    s, n3 = sub_count(r"[ \t]{2,}", " ", s)
    counts["multispaces_collapsed"] = n3

    s, n4 = sub_count(r"([?!]){2,}", r"\1", s)
    counts["multi_punct_reduced"] = n4

    s, n5 = sub_count(r"\n{3,}", "\n\n", s.strip())
    counts["multinewlines_collapsed"] = n5

    logger.info("normalize_spacing_and_punct: %s", counts)
    return s


def strip_reuters_bits(text: str) -> str:
    """
    Remove common Reuters wire-service scaffolding:

      - DATELINE lines like 'LONDON (Reuters) -'
      - WIRE PREFIX like 'UPDATE 2 - ' / 'EXCLUSIVE:'
      - Single-line BYLINE lines 'By Jane Doe'
      - TRAILING credits '(Reporting by ...; Editing by ...)'
      - TRAILING copyright lines ending with 'Reuters'

    Logs:
      * Removal counts for each pattern (dateline/byline/credit/copyright/prefix).
    """
    counts = {}

    s, n1 = DATELINE_RE.subn("", text)
    counts["dateline"] = n1

    s, n2 = WIRE_PREFIX_RE.subn("", s)
    counts["wire_prefix"] = n2

    s, n3 = BYLINE_RE.subn("", s)
    counts["byline"] = n3

    s, n4 = CREDIT_RE.subn("", s)
    counts["credits"] = n4

    s, n5 = COPY_RE.subn("", s)
    counts["copyright"] = n5

    logger.info("strip_reuters_bits: %s", counts)
    return s.strip()


def fix_linebreak_hyphens(text: str) -> str:
    """
    Fix line-break hyphenation and unwrap soft line breaks.

    - De-hyphenate words broken across a line: 'eco-\\n nomic' → 'economic'
    - Unwrap single newlines within paragraphs: 'foo\\nbar' → 'foo bar' (but
      leaves double newlines as paragraph separators)

    Logs:
      * Count of de-hyphenations and unwrap operations performed.
    """
    # de-hyphenate across linebreaks
    s, n1 = rxx.subn(r"(\p{L})-\n\s*(\p{L})", r"\1\2", text)
    # unwrap single newlines that are not paragraph boundaries
    s2, n2 = re.subn(r"([^\n])\n(?!\n)(\S)", r"\1 \2", s)

    logger.info("fix_linebreak_hyphens: dehyphen=%d, unwrap_single_newlines=%d", n1, n2)
    return s2


def normalize_dates_times(text: str) -> str:
    """
    Normalize common date and time formats and fix percent/currency spacing.

    - Dates like 'September 29, 2025' or '29 September 2025' → '2025-09-29'
    - Times like '3:05 pm' → '15:05'
    - '15 %' → '15%', '$ 10' → '$10'

    Logs:
      * Total date substitutions, time substitutions, % and $ spacing fixes.
    """
    s = text
    date_subs = 0
    for rx, repl in DATE_PATTERNS:
        s_new, n = rx.subn(repl, s)
        date_subs += n
        s = s_new

    time_subs = 0
    for rx, repl in TIME_REPLACERS:
        s_new, n = rx.subn(repl, s)
        time_subs += n
        s = s_new

    s, n_pct = re.subn(r"(\d)\s+%", r"\1%", s)
    s, n_dollar = re.subn(r"\$\s+(\d)", r"$\1", s)

    logger.info(
        "normalize_dates_times: dates=%d, times=%d, percent_space_fixes=%d, dollar_space_fixes=%d",
        date_subs,
        time_subs,
        n_pct,
        n_dollar,
    )
    return s


def conservative_spellfix(text: str, min_zipf=4.0, max_change_ratio=0.01) -> tuple[str, float]:
    """
    Apply a very conservative spelling correction focused on repeated-letter typos.

    Strategy:
      - Consider only alphabetic tokens (skip ALL-CAPS >=2 chars for tickers/initialisms).
      - If a token is rare (zipf < min_zipf), try removing a single repeated letter.
      - Accept a candidate iff it is a one-edit neighbor with zipf >= min_zipf.
      - Enforce a document-level budget: if (#changes / #alpha_tokens) > max_change_ratio,
        abort and return the original text.

    Returns
    -------
    (cleaned_text, change_ratio)

    Logs:
      * alpha_tokens_considered, proposed_changes, applied_changes (or aborted),
        and the final change_ratio.
    """
    if _NLP is not None:
        doc = _NLP.make_doc(text)  # fast tokenizer only
        tokens = [t for t in doc]
        is_alpha_flags = [t.is_alpha for t in tokens]
        token_texts = [t.text for t in tokens]
    else:
        # Fallback tokenization: words and non-space punctuation units
        token_texts = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
        is_alpha_flags = [bool(_WORD_RE.fullmatch(tok or "")) for tok in token_texts]

    def is_candidate(tok: str, is_alpha: bool) -> bool:
        if not is_alpha:
            return False
        if tok.isupper() and len(tok) >= 2:  # likely ticker/initialism
            return False
        return True

    changes = {}
    alpha_total = 0
    for i, (tok, is_alpha) in enumerate(zip(token_texts, is_alpha_flags, strict=False)):
        if not is_candidate(tok, is_alpha):
            continue
        alpha_total += 1
        lower = tok.lower()
        if zipf_frequency(lower, "en") >= min_zipf:
            continue

        cand = lower.rstrip("'")
        # Try removing a single repeated letter (e.g., 'coool' -> 'cool')
        applied = False
        for j in range(1, len(cand) - 1):
            if cand[j] == cand[j - 1]:
                candidate = cand[:j] + cand[j + 1 :]
                if (
                    zipf_frequency(candidate, "en") >= min_zipf
                    and Levenshtein.distance(cand, candidate) == 1
                ):
                    # Keep original case for leading capitalized words
                    replacement = (
                        candidate
                        if tok.islower()
                        else candidate.capitalize() if tok[0].isupper() else candidate
                    )
                    changes[i] = replacement
                    applied = True
                    break
        # We only try this one heuristic to remain conservative.

    proposed = len(changes)
    change_ratio = (proposed / max(1, alpha_total)) if alpha_total else 0.0

    if alpha_total == 0 or proposed == 0:
        logger.info(
            "conservative_spellfix: alpha_tokens=%d, proposed=0, applied=0, change_ratio=0.0",
            alpha_total,
        )
        return text, 0.0

    if change_ratio > max_change_ratio:
        logger.info(
            "conservative_spellfix: alpha_tokens=%d, proposed=%d but ABORTED (>%0.3f), applied=0, change_ratio=%0.4f",
            alpha_total,
            proposed,
            max_change_ratio,
            change_ratio,
        )
        return text, 0.0

    # Reconstruct text with applied changes, preserving original spacing via character slicing
    if _NLP is not None:
        out = []
        last = 0
        alpha_idx = 0
        for t in _NLP.make_doc(text):
            out.append(text[last : t.idx])
            tok_text = changes.get(alpha_idx, t.text) if t.is_alpha else t.text
            out.append(tok_text)
            last = t.idx + len(t.text)
            if t.is_alpha:
                alpha_idx += 1
        out.append(text[last:])
        new_text = "".join(out)
    else:
        # Fallback (no accurate char offsets) — safest to skip applying
        logger.info(
            "conservative_spellfix: spaCy unavailable; skipping application to avoid spacing errors."
        )
        return text, 0.0

    logger.info(
        "conservative_spellfix: alpha_tokens=%d, proposed=%d, applied=%d, change_ratio=%0.4f",
        alpha_total,
        proposed,
        proposed,
        change_ratio,
    )
    return new_text, change_ratio


def mask_entities(text: str) -> str:
    """
    Replace named entities with <LABEL_i> tags using spaCy NER.

    Example:
      'Apple hired John in London.' -> 'ORG_1 hired PERSON_1 in GPE_1.'

    Logs:
      * Count per entity label replaced.
    """
    if _NLP is None:
        logger.info("mask_entities: spaCy not available; no changes.")
        return text

    doc = _NLP(text)
    out = []
    last = 0
    counters = {}
    for ent in doc.ents:
        out.append(text[last : ent.start_char])
        label = ent.label_
        counters[label] = counters.get(label, 0) + 1
        out.append(f"{label}_{counters[label]}")
        last = ent.end_char
    out.append(text[last:])

    if counters:
        logger.info("mask_entities: replacements=%s", counters)
    else:
        logger.info("mask_entities: no entities found; no changes.")

    return "".join(out)


# -----------------------------------------------------------------------------
# Orchestration
# -----------------------------------------------------------------------------
@dataclass
class CleanedDocument:
    clean_text: str
    original_len: int
    clean_len: int
    spell_change_ratio: float

    def save(self, filepath: str) -> None:
        """Save the document"""
        logger.info(f"Saving cleaned text {filepath}")

        with open(filepath, "w") as f:
            f.write(self.clean_text)


class TextPreprocessor:
    """
    Text cleaning pipeline orchestrator.

    Usage:
      cfg = TextPreprocessorConfig(...)
      preprocessor = TextPreprocessor(cfg)
      clean_info = preprocessor.clean_document(raw_text)

    Methods
    -------
    clean_document(text: str) -> dict
        Apply the configured cleaning pipeline to a single document.
        Returns a dict with keys: clean_text, original_len, clean_len,
        spell_change_ratio.
    """

    def __init__(self, config: TextPreprocessorConfig):
        self.config = config

    @staticmethod
    def from_config(cfg: TextPreprocessorConfig | None = None):
        if cfg is None:
            cfg = TextPreprocessorConfig()
        return TextPreprocessor(cfg)

    def clean_document(self, text: str) -> CleanedDocument:
        """
        Apply the configured cleaning pipeline to a single document.

        Steps (gated by cfg):
        1) normalize_unicode
        2) fix_linebreak_hyphenation
        3) strip_reuters_bits (if enabled)
        4) normalize_dates_times
        5) normalize_spacing_and_punct
        6) conservative_spellfix (if enabled; may abort if budget exceeded)
        7) entity_masking (if enabled)
        8) final spacing tidy

        Returns
        -------
        dict with:
        - clean_text : str
        - original_len : int
        - clean_len : int
        - spell_change_ratio : float
        """
        cfg = self.config
        original = text
        spell_change_ratio = 0.0

        if cfg.normalize_unicode:
            text = normalize_unicode(text)
        if cfg.fix_linebreak_hyphenation:
            text = fix_linebreak_hyphens(text)
        if cfg.strip_reuters_scaffolding:
            text = strip_reuters_bits(text)
        if cfg.normalize_dates_times:
            text = normalize_dates_times(text)
        if cfg.normalize_spacing_punct:
            text = normalize_spacing_and_punct(text)

        if cfg.conservative_spelling:
            text, spell_change_ratio = conservative_spellfix(
                text, min_zipf=cfg.min_zipf_for_correction, max_change_ratio=cfg.max_change_ratio
            )

        if cfg.entity_masking:
            text = mask_entities(text)

        # final polish
        if cfg.normalize_spacing_punct:
            text = normalize_spacing_and_punct(text)

        cleaned_document = CleanedDocument(
            clean_text=text,
            original_len=len(original),
            clean_len=len(text),
            spell_change_ratio=spell_change_ratio,
        )
        return cleaned_document
