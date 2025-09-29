#! /usr/bin/env bash
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Test if a model is up and running
#
# Examples:
#   ./ping-models.sh
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

MESSAGE="Tell me a joke."
MAX_TOKENS=100
MODEL_PATH=""
PORT="8000"

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

HELP="""Script to wrap serving vllm without docker

./view-models.sh [OPTIONS]

Optional:
    -m|--model-path <str>
        Path to the model directory
    -mt|--max-tokens <int>
        Max tokens to generate (default: ${MAX_TOKENS})
    -m|--message <str>
        Message to send to the model (default: ${MESSAGE})
    -p|--port <int>
        Port to serve on (default: ${PORT})
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
    esac
done

#   Validate arguments
if [ -z "$MODEL_PATH" ]; then
    log "ERROR" "ARGS" "missing MODEL_PATH"
fi
if [ ! -d "$MODEL_PATH" ]; then
    log "ERROR" "ARGS" "MODEL_PATH $MODEL_PATH not found"
fi

#   Ping the model
log "INFO" "MAIN" "Pinging model ${MODEL_PATH} on port $PORT"

curl http://localhost:${PORT}/v1/chat/completions -H "Content-Type: application/json" -d "{
    \"model\": \"${MODEL_PATH}\",
    \"messages\": [{\"role\":\"user\",\"content\":\"${MESSAGE}\"}],
    \"max_tokens\": ${MAX_TOKENS},
    \"top_p\": 0.75,
    \"stream\": false
}"