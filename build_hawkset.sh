#!/bin/bash

source config.sh

set -e

echo Building HawkSet
cd HawkSet
docker build . -t hawkset:$HAWKSET_VERSION --build-arg PMDK_VERSION=tags/1.12.1
cd ..
docker build . -t hawkset-exp:$HAWKSET_VERSION --build-arg HAWKSET_VERSION=$HAWKSET_VERSION

echo Building Workloads
cd applications
#./full_build.sh
