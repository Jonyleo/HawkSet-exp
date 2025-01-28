#!/bin/bash

source config.sh

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        docker run --hostname=$1 --privileged -it -e "TERM=xterm-color" \
                   --workdir /root ${HAWKSET_MOUNTS} $1:$HAWKSET_VERSION
fi

