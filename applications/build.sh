#!/usr/bin/bash

source ../config.sh

docker build -t $1:$HAWKSET_VERSION . -f Dockerfile.$1 --build-arg HAWKSET_VERSION=$HAWKSET_VERSION
