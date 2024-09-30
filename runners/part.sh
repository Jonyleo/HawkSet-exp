#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm ${PM_MOUNT}/part -f

${TOOL_ROOT}/scripts/HawkSet \
	${@:1} \
	-cfg $TOOL_ROOT/config/part.cfg \
	-cfg $TOOL_ROOT/config/pmdk.cfg \
	-- \
	../durinn/third_party/RECIPE/P-ART/build/example \
	-t 8 \
	-p ${PM_MOUNT}/part \
	-i ${TOOL_ROOT}/workloads/ycsb_$WORKLOAD.txt \
	-s 1024

