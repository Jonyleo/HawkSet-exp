#!/usr/bin/bash

echo Building FAST-FAIR
./build.sh ffair
echo Building P-CLHT
./build.sh pclht
echo Building Durinn\'s target applications
./build.sh durinn
echo Building Turbohash
./build.sh turbohash
echo Building MadFS
./build.sh madfs
echo Building WIPE
./build.sh wipe
echo Building memcached-pmem
./build.sh pmemcached
echo Building apex
./build.sh apex
