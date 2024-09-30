#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm ${PM_MOUNT}/pclht -f

../scripts/HawkSet \
	${@:1} \
	-cfg $TOOL_ROOT/config/pclht.cfg \
	-cfg $TOOL_ROOT/config/pmdk.cfg \
	-- \
	../RECIPE/P-CLHT/build/example \
	-t 8 \
	-p ${PM_MOUNT}/pclht \
	-i ${TOOL_ROOT}/workloads/ycsb_$WORKLOAD.txt
