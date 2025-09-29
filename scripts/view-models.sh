#! /usr/bin/env bash
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Check to see what models are running on a server
#
# Examples:
#   ./view-models.sh
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

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
    -p|--port <int>
        Port to serve on (default: 8000)
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

        -p|--port)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PORT"
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

#   View models
log "INFO" "MAIN" "Viewing models on port $PORT"

curl http://localhost:${PORT}/v1/models