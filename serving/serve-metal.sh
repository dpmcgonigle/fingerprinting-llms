#! /usr/bin/env bash
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Serve a model with vLLM on a machine without docker
#
# Examples:
#   serve-metal.sh -mp /disk1/dma0523/models/llama3.1-8b-w4a16 -c 0
#   serve-metal.sh --default-3394
#   serve-metal.sh --default-0093
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

./serve-metal.sh [OPTIONS]

Optional:
    -c|--cuda-visible-devices <str>
        Comma-separated list of GPU ids to use, e.g. "0,1,2"
    -m|--model-path <str>
        Path to the model directory
    -p|--port <int>
        Port to serve on (default: 8000)
    --default-3394
        Shortcut for defaults on a particular server
    --default-0093
        Shortcut for defaults on a particular server
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

        -c|--cuda-visible-devices)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PYTHON"
        fi
        CUDA_VISIBLE_DEVICES=$2
        shift
        shift
        ;;
        -c=*|--cuda-visible-devices=*)
        CUDA_VISIBLE_DEVICES="${1#*=}"
        shift
        ;;

        -mp|--model-path)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PYTHON"
        fi
        MODEL_PATH=$2
        shift
        shift
        ;;
        -mp=*|--model-path=*)
        MODEL_PATH="${1#*=}"
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
        
        --default-3394)
        CUDA_VISIBLE_DEVICES="0"
        MODEL_PATH="/disk1/dma0523/models/llama3.1-8b-w4a16"
        shift
        ;;
        
        --default-0093)
        CUDA_VISIBLE_DEVICES="7"
        MODEL_PATH="/disk2/dma0523/models/llama3.1-70b-w4a16"
        shift
        ;;
    esac
done

# Validate required args
if [ -z "$MODEL_PATH" ]; then
    log "ERROR" "ARGS" "missing MODEL_PATH"
fi
if [ ! -d "$MODEL_PATH" ]; then
    log "ERROR" "ARGS" "MODEL_PATH $MODEL_PATH not found"
fi
if [ -z "$CUDA_VISIBLE_DEVICES" ]; then
    log "ERROR" "ARGS" "missing CUDA_VISIBLE_DEVICES"
fi

# Start serving
log "INFO" "MAIN" "Starting vLLM server with model $MODEL_PATH on CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES} vllm serve $MODEL_PATH \
  --tensor-parallel-size 1 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.85 \
  --port ${PORT} \
  --trust-remote-code
