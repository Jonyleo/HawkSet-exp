#!/usr/bin/bash

docker build -t $1 . -f Dockerfile.$1 --build-arg HAWKSET_VERSION=eurosys25
