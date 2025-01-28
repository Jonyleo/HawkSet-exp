#!/bin/bash

export HAWKSET_VERSION=eurosys25

HAWKSET_ROOT=`git rev-parse --show-toplevel`

export HAWKSET_ROOT

export PM_PATH=$HAWKSET_ROOT/pmem
mkdir $PM_PATH/HawkSet/pmem0 -p
mkdir $PM_PATH/HawkSet/pmem1 -p