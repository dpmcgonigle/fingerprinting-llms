#! /usr/bin/env bash
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Serve a model with vLLM on a machine without docker
#
# Examples:
#   serve-metal.sh -mp /disk1/dma0523/models/llama3.1-8b-w4a16 -c 0
#   serve-metal.sh --default-3394
#   serve-metal.sh --default-0093
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

#   DEFAULTS
PORT="8000"
GPU_MEMORY_UTILIZATION=0.85
MAX_MODEL_LEN=8192
DTYPE="auto"
EXTRA_ARGS=""
NUM_GPUS=1

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
    -mp|--model-path <str>
        Path to the model directory
    -p|--port <int>
        Port to serve on (default: $PORT)
    -g|--gpu-memory-utilization
        How much GPU memory overhead to use (default: $GPU_MEMORY_UTILIZATION)
    -mml|--max-model-len 
        Maximum model length to use (default: $MAX_MODEL_LENGTH)
    -d|--dtype
        Data Type to use (default: $DTYPE)
    -ng|--num-gpus
        Number of GPUs (default: $NUM_GPUS)
    --default-3394
        Shortcut for defaults on a particular server
    --default-0093
        Shortcut for defaults on a particular server
    --default-0094
        Shortcut for defaults on a particular server
    --0094-mixtral
        Run full mixtral on 0094
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

        -g|--gpu-memory-utilization)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PYTHON"
        fi
        GPU_MEMORY_UTILIZATION=$2
        shift
        shift
        ;;
        -g=*|--gpu-memory-utilization=*)
        GPU_MEMORY_UTILIZATION="${1#*=}"
        shift
        ;;

        -mml|--max-model-len)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PYTHON"
        fi
        MAX_MODEL_LEN=$2
        shift
        shift
        ;;
        -mml=*|--max-model-len=*)
        MAX_MODEL_LEN="${1#*=}"
        shift
        ;;

        -d|--dtype)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PYTHON"
        fi
        DTYPE=$2
        shift
        shift
        ;;
        -d=*|--dtype=*)
        NUM_GPUS="${1#*=}"
        shift
        ;;

        -ng|--num-gpus)
        if [ $# -lt 2 ]; then
            log "ERROR" "ARGS" "missing PYTHON"
        fi
        DTYPE=$2
        shift
        shift
        ;;
        -ng=*|--num-gpus=*)
        NUM_GPUS="${1#*=}"
        shift
        ;;
        
        --default-3394)
        CUDA_VISIBLE_DEVICES="0"
        MODEL_PATH="/disk1/dma0523/models/llama3.1-8b-w4a16"
        shift
        ;;
        
        --default-0093)
        CUDA_VISIBLE_DEVICES="2"
        MODEL_PATH="/disk2/dma0523/models/llama3.1-70b-w4a16"
        MAX_MODEL_LEN=4096
        PORT=8003
        shift
        ;;
        
        --0094-mixtral)
        CUDA_VISIBLE_DEVICES="5,6,7"
        MODEL_PATH="/proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1"
        MAX_MODEL_LEN=4096
        NUM_GPUS=3
        shift
        ;;
        
        --default-0094)
        log "ERROR" "ARGS" "Can't get --default-0094 working due to AWQ model issue"
        CUDA_VISIBLE_DEVICES="7"
        MODEL_PATH="/proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1-AWQ"
        DTYPE="float16"
        GPU_MEMORY_UTILIZATION=0.8
        MAX_MODEL_LEN=4096
        EXTRA_ARGS="--quantization awq"
        #EXTRA_ARGS="--chat-template templates/mixtral_chat_template.jinja --quantization awq --chat-template-content-format jinja2"
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
  --tensor-parallel-size $NUM_GPUS \
  --max-model-len $MAX_MODEL_LEN \
  --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
  --dtype $DTYPE \
  --port ${PORT} \
  --trust-remote-code \
  $EXTRA_ARGS
