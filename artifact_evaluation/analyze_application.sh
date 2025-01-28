#!/bin/bash

source ../config.sh

case $2 in
pmasstree) DOCKER_PROFILE=durinn ;;
part) DOCKER_PROFILE=durinn ;;
*) DOCKER_PROFILE=$2 ;;
esac

DOCKER_PROFILE=$DOCKER_PROFILE:$HAWKSET_VERSION
docker run --workdir /root/runners ${HAWKSET_MOUNTS} $DOCKER_PROFILE timeout 10m ./profile.sh $2 $1 $3