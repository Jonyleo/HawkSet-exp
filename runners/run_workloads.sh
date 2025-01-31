#!/bin/bash

OUTPUT=$TOOL_ROOT/$1
APP=$2
WORKLOAD_PATH=$TOOL_ROOT/$3
KICKTHETIRES=$4

if [ -z $KICKTHETIRES ] ; then
	SEED_MAX=1000
else
	SEED_MAX=10

	echo Running seed analysis for Kick-the-tires
fi

mkdir $OUTPUT -p
rm $OUTPUT/* -f

SEED_ID=0

for LOAD_FILE in ${WORKLOAD_PATH}/* ; do
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
			-unpersisted \
			-- \
			${TOOL_ROOT}/FAST_FAIR/concurrent_pmdk/btree_concurrent_mixed \
			-t 8 \
			-p ${PM_MOUNT}/ffair \
			-i $LOAD_FILE \
			2> $info \
			> /dev/null
	fi


	SEED_ID=$(expr $SEED_ID + 1)

	if [ $SEED_ID -eq $SEED_MAX ] ; then
		exit
	fi
done
