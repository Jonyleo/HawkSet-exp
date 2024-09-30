#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm ${PM_MOUNT}/* -f

../scripts/HawkSet \
 	${@:1} \
 	-cfg $TOOL_ROOT/config/turbohash.cfg \
	-cfg $TOOL_ROOT/config/pmdk.cfg \
 	-- \
	../TurboHash/release/workload \
	-i ../workloads/ycsb_$WORKLOAD.txt \
	-t 8

# ../TurboHash/release/fixme  \
# --thread=16 \
# --benchmarks=load,ycsba,delete,rehash,gc \
# --read=1000 \
# --write=1000 \
# --stats_interval=100 \
# --num=10000 \
# --bucket_count=256 \
# --cell_count=8 \
# --no_rehash=false
