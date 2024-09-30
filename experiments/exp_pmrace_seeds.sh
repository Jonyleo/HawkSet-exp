#!/usr/bin/bash

# Run all seeds under pmrace

run_experiment() {
	APP=$1
	START=$2
	END=$3

	HOST_RESULTS_FOLDER=`pwd`/pmrace_results/seeds/$1/$START
	CONTAINER_RESULTS_FOLDER=/home/vagrant/results

	OUTPUT_MOUNT=$HOST_RESULTS_FOLDER:$CONTAINER_RESULTS_FOLDER
	PMRACE_COMMAND="bash ./scripts/run_pmrace_seeds.sh $CONTAINER_RESULTS_FOLDER $APP $START $END"

	docker run --workdir /home/vagrant "-v$OUTPUT_MOUNT" pmrace $PMRACE_COMMAND 
}

run_experiment_parallel() {
	APP=$1
	N_REPLICAS=$2
	if [ $APP = "pclht" ] ; then
		SEED_APP="pclht"
	fi
	if [ $APP = "fast_fair" ] ; then
		SEED_APP="ff"
	fi
	SEED_DIR="pmrace-vagrant/seeds/full/$SEED_APP/"

	N_WORKLOADS=`ls $SEED_DIR | wc -l`
	N_PER=`expr $N_WORKLOADS / $N_REPLICAS`
	N_LAST=`expr $N_WORKLOADS % $N_REPLICAS + $N_PER`

	FIRST_SEED=`ls $SEED_DIR | head -1`
	START=${FIRST_SEED:3:6}

	PROCS=""

	for repeat in $(seq 2 $N_REPLICAS) ; do
		run_experiment $APP $START `expr $START + $N_PER - 1` &
		PROCS+=" "$!
		START=`expr $START + $N_PER` 
	done
	run_experiment $APP $START `expr $START + $N_LAST - 1` &
	PROCS+=" "$!

	wait $PROCS
}

run_experiment_parallel fast_fair 8
