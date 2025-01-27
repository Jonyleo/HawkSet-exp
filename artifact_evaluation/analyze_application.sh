#!/bin/bash

source setup.sh

set +x

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


case $2 in
pmasstree) DOCKER_PROFILE=durinn ;;
part) DOCKER_PROFILE=durinn ;;
*) DOCKER_PROFILE=$2 ;;
esac

DOCKER_PROFILE=$DOCKER_PROFILE:$HAWKSET_VERSION
docker run --workdir /root/runners ${mounts} $DOCKER_PROFILE timeout 10m ./profile.sh $2 $1 $3
unset DOCKER_PROFILE
