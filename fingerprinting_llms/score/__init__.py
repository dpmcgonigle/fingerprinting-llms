import os
import logging
from pathlib import Path

import numpy as np
import numpy.typing as npt
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class LogProbs:
    decoded_tokens: npt.NDArray[np.str_]
    token_ids: npt.NDArray[np.int32]
    token_ranks: list[np.int16]
    token_probs: list[np.float32]

    @property
    def size(self) -> int:
        return len(self.token_probs)
    
    def from_lists(
        decoded_tokens: list[str],
        token_ids: list[int],
        token_ranks: list[int],
        token_probs: list[int],
    ) -> "LogProbs":
        """Create a LogProbs
        """
        arr_decoded = np.asarray(
            decoded_tokens, dtype=np.str_
        )  # saves/loads without pickle
        arr_ids = np.asarray(token_ids, dtype=np.int32)
        arr_ranks = np.asarray(token_ranks, dtype=np.int16)
        arr_probs = np.asarray(token_probs, dtype=np.float32)  # allow np.nan / -np.inf

        logger.info(f"decoded_tokens.size {arr_decoded.size}")
        logger.info(f"token_ids.size {arr_ids.size}")
        logger.info(f"token_ranks.size {arr_ranks.size}")
        logger.info(f"token_probs.size {arr_probs.size}")
        assert arr_decoded.size == arr_ids.size == arr_ranks.size == arr_probs.size
        return LogProbs(
            decoded_tokens=arr_decoded,
            token_ids=arr_ids,
            token_ranks=arr_ranks,
            token_probs=arr_probs,
        )

    def save_npz(self, filepath: str | Path, *, compressed: bool = True) -> None:
        """
        Save this LogProbs instance to a NumPy .npz file.

        Arrays written:
          - decoded_tokens : np.ndarray[str]   (Unicode)
          - token_ids      : np.int32
          - token_ranks    : np.int16
          - token_probs    : np.float32  (use NaN or -inf for missing)

        Args:
            filepath: Output file path (e.g., "data/tokens_npz/<doc_id>.npz").
            compressed: If True, uses np.savez_compressed (smaller on disk).

        Raises:
            ValueError: if array lengths are inconsistent.
        """
        n = len(self.decoded_tokens)
        if not (len(self.token_ids) == len(self.token_ranks) == len(self.token_probs) == n):
            raise ValueError(
                f"Inconsistent lengths: decoded_tokens={n}, "
                f"token_ids={len(self.token_ids)}, "
                f"token_ranks={len(self.token_ranks)}, "
                f"token_probs={len(self.token_probs)}"
            )

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        saver = np.savez_compressed if compressed else np.savez
        logger.info(f"Saving to {filepath} with compressed {compressed}")
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath, exist_ok=True)
        saver(
            filepath,
            decoded_tokens=self.decoded_tokens,
            token_ids=self.token_ids,
            token_ranks=self.token_ranks,
            token_probs=self.token_probs,
        )


    @staticmethod
    def from_file(path: str | Path) -> "LogProbs":
        """
        Load a LogProbs instance from a NumPy .npz file created by `save_npz`.

        Args:
            path: Path to the .npz file.

        Returns:
            LogProbs: reconstructed object.

        Raises:
            FileNotFoundError: if the file does not exist.
            KeyError: if required arrays are missing.
            ValueError: if array lengths are inconsistent.
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(p)

        with np.load(p) as z:
            # Required arrays
            try:
                decoded_tokens = z["decoded_tokens"]
                token_ids = z["token_ids"]
                token_ranks = z["token_ranks"]
                token_probs = z["token_probs"]
            except KeyError as e:
                raise KeyError(f"Missing array in NPZ: {e}") from e

        n = len(decoded_tokens)
        if not (len(token_ids) == len(token_ranks) == len(token_probs) == n):
            raise ValueError(
                f"Inconsistent lengths loaded: decoded_tokens={n}, "
                f"token_ids={len(token_ids)}, token_ranks={len(token_ranks)}, "
                f"token_probs={len(token_probs)}"
            )

        return LogProbs(
            decoded_tokens=decoded_tokens,
            token_ids=token_ids,
            token_ranks=token_ranks,
            token_probs=token_probs,
        )
