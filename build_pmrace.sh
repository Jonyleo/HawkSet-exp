#!/bin/bash

set -e

cd pmrace-compare

echo Building pmrace box
vagrant up

echo Building pmrace and workloads

vagrant ssh -c " ./scripts/build_pmrace.sh ; ./scripts/build_all_workloads.sh; ./scripts/build_afl.sh "

vagrant halt