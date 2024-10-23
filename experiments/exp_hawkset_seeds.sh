#!/usr/bin/bash

# Run all seeds under HawkSet

source experiments/config.sh

do_test() {

HAWKSET_POOL="$PM_PATH/HawkSet"

HAWKSET_MOUNTS="-v $HAWKSET_POOL:/mnt/pmem \
        -v $HAWKSET_POOL/pmem0:/mnt/pmem0 \
        -v $HAWKSET_POOL/pmem1:/mnt/pmem1 \
        -v `pwd`/output:/root/output \
        -v `pwd`/HawkSet/examples:/root/examples \
        -v `pwd`/HawkSet/src:/root/src \
        -v `pwd`/HawkSet/scripts:/root/scripts \
        -v `pwd`/runners:/root/runners \
        -v `pwd`/workloads:/root/workloads \
        -v `pwd`/config:/root/config"


docker run -it $HAWKSET_MOUNTS --env WORKLOAD_PATH="/workloads/ff-seeds-old/*" --workdir /root/runners ffair ./pmrace_compare.sh /root/output/ff_seeds fast_fair 10000
mv output/ff_seeds output/ff_seeds_$1
}

for i in $(seq 1 10) ; do
	do_test $i
done
