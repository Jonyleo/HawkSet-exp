#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm /mnt/pmem0/baotong/template.data -f
mkdir /mnt/pmem0/baotong -p

PM_MOUNT=/mnt/pmem0 \
LD_PRELOAD=${TOOL_ROOT}/apex/build_debug/pmdk/src/PMDK/src/debug/libpmemobj.so.1 \
../scripts/HawkSet \
	${@:1} \
	-cfg ${TOOL_ROOT}/config/apex.cfg \
	-- \
	${TOOL_ROOT}/apex/build_debug/benchmark \
	-t 8 \
	-i ${TOOL_ROOT}/workloads/ycsb_$WORKLOAD.txt \
	-k ${TOOL_ROOT}/ycsb-200M.bin
