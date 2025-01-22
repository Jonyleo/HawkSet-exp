#!/bin/bash

source setup.sh

mkdir $PM_PATH/HawkSet/pmem0 -p
mkdir $PM_PATH/HawkSet/pmem1 -p

HAWKSET_POOL=$PM_PATH/HawkSet

mounts="-v $HAWKSET_POOL:/mnt/pmem \
        -v $HAWKSET_POOL/pmem0:/mnt/pmem0 \
        -v $HAWKSET_POOL/pmem1:/mnt/pmem1 \
        -v $HAWKSET_ROOT/output:/root/output \
        -v $HAWKSET_ROOT/HawkSet/examples:/root/examples \
        -v $HAWKSET_ROOT/HawkSet/src:/root/src \
        -v $HAWKSET_ROOT/HawkSet/scripts:/root/scripts \
        -v $HAWKSET_ROOT/runners:/root/runners \
        -v $HAWKSET_ROOT/workloads:/root/workloads \
        -v $HAWKSET_ROOT/config:/root/config"


single_test() {
	if [ -z $DOCKER_PROFILE ] ; then
		DOCKER_PROFILE=$1
	fi
        DOCKER_PROFILE=$DOCKER_PROFILE:hawkset-$HAWKSET_VERSION
        docker run --workdir /root/runners ${mounts} $DOCKER_PROFILE timeout 10m ./profile.sh $1 $report_folder $2
	unset DOCKER_PROFILE
}

# Fresh build
docker run --workdir /root/scripts ${mounts} hawkset-exp:$HAWKSET_VERSION sh -c  "./clean.sh && ./build.sh"

full_test() {
        single_test ffair
        single_test pclht
        single_test turbohash
        single_test pmasstree
        single_test madfs zipf_4k
	DOCKER_PROFILE=durinn single_test part
        single_test pmemcached
	single_test wipe
	single_test apex
}


for i in $(seq 1 $2) ; do
        report_folder=../output/$1/run_$i
        full_test
done
