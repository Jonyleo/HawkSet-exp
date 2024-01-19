#!/bin/bash


OUTPUT=$1

mkdir $OUTPUT -p

for LOAD_FILE in ${TOOL_ROOT}/workloads/ycsb_16*
do
	echo $LOAD_FILE
	TMP=${LOAD_FILE##*_}
	LOAD=${TMP%%.*}

	info=$OUTPUT/$LOAD-irh1.info
	log=$OUTPUT/$LOAD-irh1.log

	echo "-------------------------" 
	echo "app: ffair, heuristics: IRH, LOAD: $LOAD" 

	rm ${PM_MOUNT}/ffair -f

	PROFILE=1 \
	./HawkSet \
		-out $log \
		${@:1} \
		-- \
		./../FAST_FAIR/concurrent_pmdk/btree_concurrent_mixed \
		-t 8 \
		-p ${PM_MOUNT}/ffair \
		-i ${TOOL_ROOT}/workloads/ycsb_$LOAD.txt \
		2> $info \
		> /dev/null

done
