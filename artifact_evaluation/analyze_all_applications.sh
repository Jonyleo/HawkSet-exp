#!/bin/bash

source ../config.sh

analyze_all_applications_once () {
        ./analyze_application.sh $report_folder ffair
        ./analyze_application.sh $report_folder pclht
        ./analyze_application.sh $report_folder turbohash
        ./analyze_application.sh $report_folder pmasstree
        ./analyze_application.sh $report_folder madfs zipf_4k
	./analyze_application.sh $report_folder part
        ./analyze_application.sh $report_folder pmemcached
	./analyze_application.sh $report_folder wipe
	./analyze_application.sh $report_folder apex
}

for i in $(seq 1 5) ; do
        report_folder=../output/reports/run_$i
        analyze_all_applications_once
done
