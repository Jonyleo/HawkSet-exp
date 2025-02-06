#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD="1000"
fi

if [ -z $MODE  ] ; then
        MODE="zipf_4k"
fi

rm ${PM_MOUNT}/* -f

BENCH_FILE_SIZE=1 \
BENCH_NUM_ITER=$WORKLOAD \
PMEM_PATH=${PM_MOUNT} \
MADFS_LOG_LEVEL=4 \
../scripts/HawkSet \
	${@:1} \
	-- \
	${TOOL_ROOT}/MadFS/build-debug/micro_mt \
	--benchmark_filter=$MODE \
	--benchmark_out=/dev/null
