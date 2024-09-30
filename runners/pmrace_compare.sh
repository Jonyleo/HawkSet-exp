#!/bin/bash

OUTPUT=$1
APP=$2
LIMIT=$3

mkdir $OUTPUT -p
rm $OUTPUT/* -f

#./build.sh

if [ -z WORKLOAD_PATH ] ; then
	WORKLOAD_PATH=/workloads/seed*/*---cov
	REPLACE=1
fi

for LOAD_FILE in ${TOOL_ROOT}${WORKLOAD_PATH} ; do
	if [ -z REPLACE ] ; then
		LOAD_FILE=${LOAD_FILE//cov/workload.csv}
	fi
	
	echo $LIMIT executions left
	if [ $LIMIT = 0 ] ; then
		exit
	fi
	LIMIT=$(expr $LIMIT - 1)

	TMP=${LOAD_FILE##*/}
	LOAD=${TMP%%---*}

	info=$OUTPUT/$LOAD-irh1.info
	log=$OUTPUT/$LOAD-irh1.log

	echo "------------------------------------------" 
	echo "app: $APP, heuristic: IRH, LOAD: $LOAD" 


	if [ $APP = "fast_fair" ] ; then
		rm ${PM_MOUNT}/ffair -f

		PROFILE=1 \
		${TOOL_ROOT}/scripts/HawkSet \
			-out $log \
			-- \
			${TOOL_ROOT}/FAST_FAIR/concurrent_pmdk/btree_concurrent_mixed \
			-t 8 \
			-p ${PM_MOUNT}/ffair \
			-i $LOAD_FILE \
			2> $info \
			> /dev/null
	fi
	if [ $APP = "pclht" ] ; then
		rm ${PM_MOUNT}/pclht -f
		
		PROFILE=1 \
		${TOOL_ROOT}/scripts/HawkSet \
			-out $log \
			-cfg $TOOL_ROOT/config/pclht.cfg \
			-cfg $TOOL_ROOT/config/pmdk.cfg \
			-- \
			${TOOL_ROOT}/RECIPE/P-CLHT/build/example \
			-t 8 \
			-p ${PM_MOUNT}/pclht \
			-i $LOAD_FILE \
			2> $info \
			> /dev/null
	fi
done
