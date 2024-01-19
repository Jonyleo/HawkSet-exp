#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm ${PM_MOUNT}/ffair -f

../scripts/HawkSet \
	${@:1} \
	-- \
	./../FAST_FAIR/concurrent_pmdk/btree_concurrent_mixed \
	-t 8 \
	-p ${PM_MOUNT}/ffair \
	-i ${TOOL_ROOT}/workloads/ycsb_$WORKLOAD.txt
