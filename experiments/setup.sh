#!/bin/bash

set -e

HAWKSET_ROOT=`pwd`

if [[ $HAWKSET_ROOT == *"experiments"* ]] ; then
	HAWKSET_ROOT=$HAWKSET_ROOT/..
fi

source $HAWKSET_ROOT/config.sh
export HAWKSET_ROOT