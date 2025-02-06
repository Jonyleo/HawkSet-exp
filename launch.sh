#!/bin/bash

source config.sh

HAWKSET_MOUNTS="$HAWKSET_MOUNTS -v $HAWKSET_ROOT/pmrace-compare/download/pmrace_results:/root/pmrace_results"

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        docker run --hostname=$1 --privileged -it -e "TERM=xterm-color" \
                   --workdir /root ${HAWKSET_MOUNTS} $1:$HAWKSET_VERSION
fi

