#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm ${PM_MOUNT}/pmass -f

../scripts/HawkSet \
	${@:1} \
	-cfg $TOOL_ROOT/config/pmdk.cfg \
	-- \
	../durinn/third_party/RECIPE/P-Masstree/build/example \
	-t 8 \
	-p ${PM_MOUNT}/pmass \
	-i ${TOOL_ROOT}/workloads/ycsb_$WORKLOAD.txt \
	-s 1024

