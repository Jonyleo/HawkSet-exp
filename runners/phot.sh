#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm ${PM_MOUNT}/phot -f

../scripts/HawkSet \
	${@:1} \
	-cfg $TOOL_ROOT/config/phot.cfg \
	-cfg $TOOL_ROOT/config/pmdk.cfg \
	-- \
	../durinn/third_party/RECIPE/P-HOT/build/example \
	-t 8 \
	-p ${PM_MOUNT}/phot \
	-i ${TOOL_ROOT}/workloads/ycsb_$WORKLOAD.txt \
	-s 1024

