#!/bin/bash

source ../config.sh

KICKTHETIRES=$1

run_pmrace_seeds() {
	cd ../pmrace-compare
	vagrant up

	vagrant ssh  -c " ./scripts/exp_seed_seperate.sh $KICKTHETIRES"

	vagrant halt
	cd ../artifact_evaluation
}

run_hawkset_seeds() {
	docker run --workdir /root/runners ${HAWKSET_MOUNTS} ffair:$HAWKSET_VERSION timeout 10m ./run_workloads.sh output/pmrace_seeds/ffair fast_fair workloads/seeds-pmrace-ffair $KICKTHETIRES
}

if [ -z $KICKTHETIRES ] ; then
	echo "Analyzing PMRace: Estimated time - 48h. Are you running tmux?"
	read -p "Proceed? [y/n]: " PROCEED

	if [[ $PROCEED != y ]] ; then
		exit
	fi
fi

run_pmrace_seeds
run_hawkset_seeds