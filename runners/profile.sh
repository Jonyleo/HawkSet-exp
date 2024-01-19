#!/bin/bash

APP=$1
OUTPUT=$2/$APP
if [[ ! -z $3 ]] ; then
	OUTPUT=$OUTPUT-$3
fi

if [ -z "$WORKLOADS" ] ; then
	WORKLOADS="1000 10000 100000"
fi

if [ -z "$HEURISTICS" ] ; then
        HEURISTICS="0 1"
fi

mkdir $OUTPUT -p

for LOAD in $WORKLOADS
do
	for HEURISTIC in $HEURISTICS
	do
		info=$OUTPUT/$LOAD-irh$HEURISTIC.info
		log=$OUTPUT/$LOAD-irh$HEURISTIC.log

		echo "-------------------------" 
		echo "app: $APP, heuristics: $HEURISTIC, LOAD: $LOAD" 

		PROFILE=1 \
		MODE=$3 \
		WORKLOAD=$LOAD \
			./$APP.sh \
			-irh $HEURISTIC \
			-out $log \
			> /dev/null \
			2> $info

	done
done
