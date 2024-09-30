import os
import sys
import glob
from parse_races import parse_bugs
from utils import *

if __name__ == "__main__":
	app = sys.argv[1]
	workload_dir = sys.argv[2] + os.sep + app 
	pmrace_dir = sys.argv[2] + os.sep + app + "-clean"
	hawkset_dir = sys.argv[3] + os.sep + app
	pmrace_time = int(sys.argv[4])

	n_executions = len(glob.glob(pmrace_dir + os.sep + "seed*" + os.sep + "*---cov"))
	n_workloads = 0
	n_ops = 0


	for workload in glob.glob(workload_dir + os.sep + "seed*" + os.sep + "*---workload.csv"):
		with open(workload, "r") as f_workload:
			n_workloads += 1
			n_ops += len(f_workload.readlines())


	races_found_by_pmrace = []
	for race in glob.glob(pmrace_dir + os.sep + "seed*" + os.sep + "*---race.csv.parsed"):
		if found_bug_pmrace(app, race):
			races_found_by_pmrace.append(race)



	avg_ops = n_ops / n_workloads

	hawkset_time = 0

	n_runs_hawkset = 0


	for result in glob.glob(hawkset_dir + os.sep  + "*.info"):
		n_runs_hawkset += 1
		info = extract_info(result)

		hawkset_time += info["elapsed"]

	print(hawkset_time)

	n_races_found_by_hawkset = 0
	for race in glob.glob(hawkset_dir + os.sep  + "*.log"):
		if found_bug_hawkset(app, race):
			n_races_found_by_hawkset += 1

	assert n_executions == n_runs_hawkset

# TODO change to 600

	print(races_found_by_pmrace)

	races_found_by_pmrace = len(races_found_by_pmrace)

	print(f"Workloads executed: {n_executions}")
	print(f"Average workload size (ops): {avg_ops:.0f}")

	print(f"PMRace's analysis time (per workload): {pmrace_time / n_executions:.4f} s")
	print(f"PMRace's analysis time (total): {pmrace_time} s")	
	print(f"PMRace's bug finding efficacy: {races_found_by_pmrace / n_executions * 100:.2f}% ({races_found_by_pmrace} out of {n_executions})")	
	print(f"Avg time to detect race: {pmrace_time / (races_found_by_pmrace):.2f}")

	print(f"HawkSet's analysis time (per workload): {hawkset_time / n_executions:.4f} s")
	print(f"HawkSet's analysis time (total): {hawkset_time:.4f} s")
	print(f"HawkSet's bug finding efficacy: {n_races_found_by_hawkset / n_executions * 100:.2f}% ({n_races_found_by_hawkset} out of {n_executions})")	
	print(f"Avg time to detect race: {hawkset_time / (n_races_found_by_hawkset):.2f}")

	print(f"Execution speedup: {pmrace_time / hawkset_time:.2f}x")
	print(f"Overall speedup: {hawkset_time / pmrace_time  * (n_races_found_by_hawkset / races_found_by_pmrace):.2f}x")

	
