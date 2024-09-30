#!/usr/bin/bash

TIME=$1
EXTRA_TIME=$(expr $TIME + $TIME / 10)

compare_app() {
	# $1 app

	PMRACE_RESULT=`pwd`/../pmrace_results/$1
	mkdir $PMRACE_RESULT -p

	echo $EXTRA_TIME
	if [ $1 = "pclht" ] ; then
		OUTPUT_MOUNT=$PMRACE_RESULT:/home/vagrant/pm-workloads/RECIPE/P-CLHT/build/output
		CONTAINER=pclht
		FOLDER=/home/vagrant/pm-workloads/RECIPE
	fi
	if [ $1 = "fast_fair" ] ; then
		OUTPUT_MOUNT=$PMRACE_RESULT:/home/vagrant/pm-workloads/FAST_FAIR/concurrent_pmdk/output
		CONTAINER=ffair
		FOLDER=/home/vagrant/pm-workloads/FAST_FAIR
	fi

 	echo "cp $FOLDER-clean/* $FOLDER -r && timeout $TIME ./scripts/debug_workload.sh $1 sample" | \
	docker run --rm -i --workdir /home/vagrant "-v$OUTPUT_MOUNT" pmrace bash -s

	mv $PMRACE_RESULT $PMRACE_RESULT-clean

	echo "cp $FOLDER-dirty/* $FOLDER -r && timeout $EXTRA_TIME ./scripts/debug_workload.sh $1 sample" | \
	docker run --rm -i --workdir /home/vagrant "-v$OUTPUT_MOUNT" pmrace bash -s

	HAWKSET_POOL="/mnt/pmem1/HawkSet"
	HAWKSET_MOUNTS="-v $HAWKSET_POOL:/mnt/pmem \
			        -v $HAWKSET_POOL/pmem0:/mnt/pmem0 \
			        -v $HAWKSET_POOL/pmem1:/mnt/pmem1 \
					-v $PMRACE_RESULT:/root/workloads \
	     		    -v `pwd`/../config:/root/config \
	        		-v `pwd`/../output:/root/output \
	        		-v `pwd`/../runners:/root/runners \
			        -v `pwd`/../HawkSet/src:/root/src \
			        -v `pwd`/../HawkSet/scripts:/root/scripts"

	n_runs=0

	for run in $PMRACE_RESULT-clean/seed*/seed*-inter*-run*---cov ; do
		n_runs=$(expr $n_runs + 1)
	done

	echo Executed $n_runs times

	docker run -it  $HAWKSET_MOUNTS --workdir /root/runners $CONTAINER /usr/bin/bash ./pmrace_compare.sh /root/output/$1 $1 $n_runs
 }

compare_app fast_fair

#compare_app pclht

echo "Results for Fast-Fair"
python3 scripts/disp_pmrace_compare.py fast_fair `pwd`/../pmrace_results `pwd`/../output $TIME

# echo
# echo "Results for P-CLHT"
# python3 scripts/disp_pmrace_compare.py pclht `pwd`/../pmrace_results `pwd`/../output
