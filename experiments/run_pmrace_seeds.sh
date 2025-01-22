#!/bin/bash

source setup.sh

RESULTS_FOLDER=$1
APP=$2
START=$3
END=$4

rm -rf $RESULTS_FOLDER/*

SEED_DIR=$PMRACE_ROOT/seeds
PM_WORKLOADS_DIR=$PMRACE_ROOT/pm-workloads

if [ $APP = "pclht" ] ; then
	WORK_DIR=$PM_WORKLOADS_DIR/RECIPE/P-CLHT/build
	TIME=5m
	SEED_APP="pclht"
fi
if [ $APP = "fast_fair" ] ; then
	WORK_DIR=$PM_WORKLOADS_DIR/FAST_FAIR/concurrent_pmdk
	TIME=10m
	SEED_APP="ff"
fi

OUTPUT=$WORK_DIR/output

rm $SEED_DIR/sample/$SEED_APP/*

echo $START "->" $END ":" Starting 

for id in $(seq -f %06g $START $END) ; do
	SEED=$SEED_DIR/full/$SEED_APP/id:$id*
	CUR_RESULTS_FOLDER=$RESULTS_FOLDER/$id

	mkdir -p $CUR_RESULTS_FOLDER

	cp $SEED $SEED_DIR/sample/$SEED_APP/


	timeout $TIME ./scripts/debug_workload.sh $APP sample &> $CUR_RESULTS_FOLDER/output.log

	cp $OUTPUT/seed*/*---workload.csv $CUR_RESULTS_FOLDER &> /dev/null
	cp $OUTPUT/seed*/*---race.csv.parsed $CUR_RESULTS_FOLDER &> /dev/null

	cd $WORK_DIR
	python3 $PMRACE_ROOT/pmrace/scripts/find_bugs.py output report | tail -n 1 > $CUR_RESULTS_FOLDER/bug_count.txt
	cd $PMRACE_ROOT

	rm $SEED_DIR/sample/$SEED_APP/*
done

echo $START "->" $END ":" Ending
