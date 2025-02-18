#!/bin/bash

source ../config.sh

KICKTHETIRES=$1

run_pmrace_seeds() {
	if [ -z $KICKTHETIRES ] ; then
		echo "Analyzing PMRace: Estimated time - 48h. Are you running tmux?"
		echo "Restarting this experiment again will destroy previous results."
		read -p "Proceed? [y/n]: " PROCEED

		if [[ $PROCEED != y ]] ; then
			exit
		fi
	fi

	HAWKSET_MOUNTS="$HAWKSET_MOUNTS -v $HAWKSET_ROOT/pmrace-compare/download:/root/to_delete"

	docker run --hostname=hawkset --privileged -e "TERM=xterm-color" \
	                   --workdir /root ${HAWKSET_MOUNTS} hawkset:$HAWKSET_VERSION \
	                   -c "echo Cleaning previous results ; rm to_delete/pmrace_results -rf"

	cd ../pmrace-compare
	vagrant up

	vagrant ssh  -c " ./scripts/exp_seed_seperate.sh $KICKTHETIRES"

	vagrant halt
	cd ../artifact_evaluation
}

run_hawkset_seeds() {
	docker run --workdir /root/runners ${HAWKSET_MOUNTS} ffair:$HAWKSET_VERSION ./run_workloads.sh output/pmrace_seeds/ffair fast_fair workloads/seeds-pmrace-ffair $KICKTHETIRES
}



run_pmrace_seeds
run_hawkset_seeds
