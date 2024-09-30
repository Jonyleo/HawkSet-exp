#!/usr/bin/bash

# Run all seeds under HawkSet

HAWKSET_POOL="/mnt/pmem1/HawkSet"
HAWKSET_MOUNTS="-v $HAWKSET_POOL:/mnt/pmem \
		        -v $HAWKSET_POOL/pmem0:/mnt/pmem0 \
		        -v $HAWKSET_POOL/pmem1:/mnt/pmem1 \
     		    -v "$(pwd)"/workloads:/root/workloads \
     		    -v "$(pwd)"/config:/root/config \
        		-v "$(pwd)"/output:/root/output \
        		-v "$(pwd)"/runners:/root/runners \
		        -v "$(pwd)"/HawkSet/src:/root/src \
		        -v "$(pwd)"/HawkSet/scripts:/root/scripts"

docker run -it $HAWKSET_MOUNTS --env WORKLOAD_PATH="/workloads/pmrace/*" --workdir /root/runners ffair /usr/bin/bash ./pmrace_compare.sh /root/output/ff_seeds fast_fair 10000
