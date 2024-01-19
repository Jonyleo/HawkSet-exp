source config.sh

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
        
docker run --privileged -it --workdir /root ${mounts} $1
