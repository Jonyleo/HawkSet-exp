#!/bin/bash

source experiments/config.sh

HAWKSET_POOL="$PM_PATH/HawkSet"

mounts="-v $HAWKSET_POOL:/mnt/pmem \
        -v $HAWKSET_POOL/pmem0:/mnt/pmem0 \
        -v $HAWKSET_POOL/pmem1:/mnt/pmem1 \
        -v `pwd`/output:/root/output \
        -v `pwd`/HawkSet/examples:/root/examples \
        -v `pwd`/HawkSet/src:/root/src \
        -v `pwd`/HawkSet/scripts:/root/scripts \
        -v `pwd`/runners:/root/runners \
        -v `pwd`/workloads:/root/workloads \
        -v `pwd`/config:/root/config"

docker run --hostname=$1 --privileged -it -e "TERM=xterm-color" --workdir /root/runners ${mounts} $1
