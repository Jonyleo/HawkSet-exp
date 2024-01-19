#!/bin/bash

source config.sh

mkdir $PM_MOUNT/pmem0 -p
mkdir $PM_MOUNT/pmem1 -p

mounts="-v $PM_MOUNT:/mnt/pmem \
        -v $PM_MOUNT/pmem0:/mnt/pmem0 \
        -v $PM_MOUNT/pmem1:/mnt/pmem1 \
        -v `pwd`/output:/root/output \
        -v `pwd`/HawkSet/examples:/root/examples \
        -v `pwd`/HawkSet/src:/root/src \
        -v `pwd`/HawkSet/scripts:/root/scripts \
        -v `pwd`/runners:/root/runners \
        -v `pwd`/workloads:/root/workloads \
        -v `pwd`/config:/root/config"


single_test() {
	docker run --workdir /root/runners ${mounts} $1:1.12 ./profile.sh $1 $report_folder $2
}

# Fresh build
docker run --workdir /root/scripts ${mounts} montage:1.12 sh -c  "./clean.sh && ./build.sh"

full_test() {

        # MadFS
        single_test madfs zipf_4k

        # Key-value Stores
        single_test pclht
        single_test ffair
        single_test turbohash
        single_test montage MontageQueue
        single_test montage MontageHashTable
        single_test montage MontageGraph-Custom

}

for i in $(seq 1 $1) ; do
	report_folder=../output/full_exp/run_$i
	full_test
done
