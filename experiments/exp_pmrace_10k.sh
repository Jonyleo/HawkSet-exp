#!/usr/bin/bash

source setup.sh

run_pmrace() {
	PMRACE_RESULT=`pwd`/pmrace_results/$1


	if [ $1 = "pclht" ] ; then
		OUTPUT_MOUNT=$PMRACE_RESULT:/home/vagrant/pm-workloads/RECIPE/P-CLHT/build/output
		CONTAINER=pclht
	fi
	if [ $1 = "fast_fair" ] ; then
		OUTPUT_MOUNT=$PMRACE_RESULT:/home/vagrant/pm-workloads/FAST_FAIR/concurrent_pmdk/output
		CONTAINER=ffair
	fi

	WORKLOAD_MOUNT=`pwd`/workloads:/home/vagrant/seeds/big
	
	

	docker run -it --workdir /home/vagrant "-v$OUTPUT_MOUNT" "-v$WORKLOAD_MOUNT" pmrace  
}

run_pmrace fast_fair 
