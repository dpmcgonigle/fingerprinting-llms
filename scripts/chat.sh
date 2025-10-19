#! /usr/bin/env bash
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Test if a model is up and running
#
# Examples:
#   ./chat.sh -mp "/disk2/dma0523/models/llama3.1-70b-w4a16" -p 9003
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

#   VARIABLES
MESSAGE="Tell me a joke."
MAX_TOKENS=2000
MODEL_PATH=""
PORT="8000"
USE_JQ=true
OUTPUTFILE=""

############	functions	##############
function datetimestamp() {
    printf "$(date -u +'%m/%d/%Y %H:%M:%S')"
}
function log() {
    #   $1: log level
    #   $2: log source script/function
    #   $3: log message
    if [ "$1" == "ERROR" ]; then
        printf "[${1}] [$(datetimestamp)] [${2}] : ${3}\n" >&2
        printf "$HELP"
        exit 1
    else
	    printf "[${1}] [$(datetimestamp)] [${2}] : ${3}\n"
    fi
}

HELP="""Script to wrap chat compleation from a model running on VLLM

./view-models.sh [OPTIONS]

Optional:
    -mp|--model-path <str>
        Path to the model directory
    -mt|--max-tokens <int>
        Max tokens to generate (default: ${MAX_TOKENS})
    -m|--message <str>
        Message to send to the model (default: ${MESSAGE})
    -p|--port <int>
        Port model is served on (default: ${PORT})
    -o|--output-file
        File to output response to
    -h|--help
        Print this help message"""

# Parse CLI Arguments
while [ $# -gt 0 ]
do
    key="$1"

    case $key in

        -h|--help)
        printf "%s" "${HELP}"
        exit 1;
        ;;

        -mp|--model-path)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing MODEL_PATH"
        fi
        MODEL_PATH=$2
        shift
        shift
        ;;
        -mp=*|--model-path=*)
        MODEL_PATH="${1#*=}"
        shift
        ;;

        -mt|--max-tokens)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing MAX_TOKENS"
        fi
        MAX_TOKENS=$2
        shift
        shift
        ;;
        -mt=*|--max-tokens=*)
        MAX_TOKENS="${1#*=}"
        shift
        ;;

        -m|--message)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing MESSAGE"
        fi
        MESSAGE=$2
        shift
        shift
        ;;
        -m=*|--message=*)
        MESSAGE="${1#*=}"
        shift
        ;;

        -p|--port)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PYTHON"
        fi
        PORT=$2
        shift
        shift
        ;;
        -p=*|--port=*)
        PORT="${1#*=}"
        shift
        ;;

        -o|--output-file)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PYTHON"
        fi
        OUTPUTFILE=$2
        shift
        shift
        ;;
        -o=*|--output-file=*)
        OUTPUTFILE="${1#*=}"
        shift
        ;;
    esac
done

#   Validate arguments
if [ -z "$MODEL_PATH" ]; then
    log "ERROR" "ARGS" "missing MODEL_PATH"
fi

#   Ping the model
log "INFO" "MAIN" "Pinging model ${MODEL_PATH} on port $PORT"

# JSON-escape the message using sed (handles \ " tabs CR LF and general backslashes)
json_escape() {
  awk 'BEGIN{ORS=""; sep=""}
       { gsub(/\\/,"\\\\"); gsub(/"/,"\\\""); gsub(/\t/,"\\t"); gsub(/\r/,"\\r");
         printf "%s%s", sep, $0; sep="\\n" }
       END{print ""}'
}
ESCAPED_MESSAGE="$(printf '%s' "$MESSAGE" | json_escape)"

RESPONSE=$(curl http://localhost:${PORT}/v1/chat/completions -H "Content-Type: application/json" -d "{
    \"model\": \"${MODEL_PATH}\",
    \"messages\": [{\"role\":\"user\",\"content\":\"${ESCAPED_MESSAGE}\"}],
    \"max_tokens\": ${MAX_TOKENS},
    \"top_p\": 0.75,
    \"stream\": false
}")

if [ "$USE_JQ" == "true" ]; then
    log "INFO" "MAIN" "Performing jq on $RESPONSE"
    RESPONSE=$(printf '%s' "$RESPONSE" | jq -r '.choices[0].message.content // .choices[0].text // empty')
fi

if [ ! -z "$OUTPUTFILE" ]; then
    mkdir -p $(dirname $OUTPUTFILE)
    printf '%s' "$RESPONSE" > $OUTPUTFILE
else
    log "INFO" "MAIN" "$RESPONSE"
fi