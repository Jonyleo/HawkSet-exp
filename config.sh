#!/bin/bash

export HAWKSET_VERSION=eurosys25

export HAWKSET_ROOT=`git rev-parse --show-toplevel`

export PM_PATH=$HAWKSET_ROOT/pmem

export HAWKSET_POOL="$PM_PATH/HawkSet"

mkdir $HAWKSET_POOL/pmem0 -p
mkdir $HAWKSET_POOL/pmem1 -p

export HAWKSET_MOUNTS="-v $HAWKSET_POOL:/mnt/pmem \
        -v $HAWKSET_POOL/pmem0:/mnt/pmem0 \
        -v $HAWKSET_POOL/pmem1:/mnt/pmem1 \
        -v $HAWKSET_ROOT/output:/root/output"