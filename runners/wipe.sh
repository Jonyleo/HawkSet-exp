#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm ${PM_MOUNT}/wipe -f
mkdir /mnt/pmem1/lbl/ -p

PM_MOUNT=/mnt/pmem1 ${TOOL_ROOT}/scripts/HawkSet \
	${@:1} \
	-- \
	${TOOL_ROOT}/WIPE/build/example \
	-t 8 \
	-i ${TOOL_ROOT}/workloads/ycsb_${WORKLOAD}.txt
