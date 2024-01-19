#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=1000
fi

rm ${PM_MOUNT}/* -f

./HawkSet \
	${@:1} \
	-- \
	../Montage/bin/main \
	-R $MODE \
	-M $MODE:$WORKLOAD \
	-t 8 \
	-dPersistStrat=DirWB \
	-dEpochLength=1000 \
	-v 
