#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm -rf /mnt/pmem0/*

rm -f /dev/shm/*_shared /dev/shm/psegments/*

rm -rf /mnt/pmem0/libpuddles
mkdir -p /mnt/pmem0/libpuddles

export LIBPUDDLES_PUDDLED_PORT=1234
export LIBPUDDLES_DIR=${TOOL_ROOT}/libpuddles-ae/libpuddles

echo 1 | sudo tee /proc/sys/vm/unprivileged_userfaultfd

if [ -z ${LIBPUDDLES_DIR+x} ]; then
    echo "LIBPUDDLES_DIR is unset";
    exit 1
fi

export LIBPUDDLES_PUDDLED_PORT=2000
export LIBPUDDLES_LOG_LEVEL=0
export LIBPUDDLES_NO_PUDDLE_RELEASE=1
export LIBPUDDLES_NO_STACKTRACE=1
export LIBPUDDLES_NO_USERFAULTD=1
export LIBPUDDLES_FORCE_NO_PERSIST=0
export LIBPUDDLES_FORCE_CLWB=1
export LIBPUDDLES_BUDDY_VERIFY=0
export LIBPUDDLES_LOG_WILDCARD="*"
export LIBPUDDLES_GEN_STATS=0
export LIBPUDDLES_ENABLE_HYBRID_LOGGING=0

export HUNDRED_K=100000
export MILLION=1000000
export TEN_MILLION=10000000

CMN_CMD="$0"

CMN_SCRIPT_NAME="${EXPERIMENT_NAME:-$(basename "${CMN_CMD}")}"
WORKLOAD_NAME="$(echo "${CMN_SCRIPT_NAME}" | sed 's/.sh//')"

COMMON_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RESULTS_DIR="${COMMON_DIR}/data/${WORKLOAD_NAME}"
mkdir -p "${RESULTS_DIR}"

CMN_LOG_FILE="run.log"
SCRIPTS_ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"

export PATH="${PATH}:${LIBPUDDLES_DIR}"
export PATH="${PATH}:${LIBPUDDLES_DIR}/bin"
export PATH="${PATH}:${LIBPUDDLES_DIR}/bin/examples"


mkdir -p /mnt/pmem0/libpuddles
${LIBPUDDLES_DIR}/bin/puddled \
        --run ${LIBPUDDLES_PUDDLED_PORT},/mnt/pmem0/libpuddles \
        --purge --replace


${LIBPUDDLES_DIR}/bin/examples/linkedlist_tx linkedlist


# ../scripts/HawkSet \
# 	${@:1} \
# 	-- \
# 	./../FAST_FAIR/concurrent_pmdk/btree_concurrent_mixed \
# 	-t 8 \
# 	-p ${PM_MOUNT}/ffair \
# 	-i ${TOOL_ROOT}/workloads/ycsb_$WORKLOAD.txt
