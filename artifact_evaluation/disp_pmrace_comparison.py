import os
import sys
import glob
from parsing_utils import parse_all, parse_data
import math
import shutil
import logging
from bugs import found_bug_pmrace, found_bug_hawkset

# pmrace's bug finding utilities
sys.path.append("../pmrace/scripts/")
from find_bugs import find_bugs_in_outputs

def get_pmrace_data(app, results_dir):
	seeds_with_races_nr1 = 0

	# PMRace does not report bug number 2
	# See https://dl.acm.org/doi/abs/10.1145/3503222.3507755
	seeds_with_races_nr2 = 0

	seeds = glob.glob(results_dir + os.sep + "seed*")

	target = results_dir + os.sep + "target"

	for seed in seeds:
		seed_target = target + os.sep + seed.split(os.sep)[-1]
		
		shutil.move(seed, seed_target)

		has_bug = find_bugs_in_outputs(target, None, False)[0]

		if has_bug:
			seeds_with_races_nr1 += 1

		shutil.move(seed_target, results_dir)

	return seeds_with_races_nr1, seeds_with_races_nr2, len(seeds)

def get_hawkset_data(app, results_dir):
	n_racy_seeds_nr1 = 0
	n_racy_seeds_nr2 = 0
	
	bugs = parse_all(results_dir, None)

	if app not in bugs:
		print(f"No results found for HawkSet comparison to PMRace for {app}. Did you run the exp script?")
		exit(-1)

	bugs = bugs[app]

	for seed in bugs:
		if found_bug_hawkset(app, bugs[seed], 1):
			n_racy_seeds_nr1 += 1

		if found_bug_hawkset(app, bugs[seed], 2):
			n_racy_seeds_nr2 += 1


	data = parse_data(results_dir, None)

	total_time = sum((data[app][1][seed]["elapsed"][0] for seed in data[app][1]))

	return n_racy_seeds_nr1, n_racy_seeds_nr2, len(bugs), total_time


def avg_time_to_race(total_runs, racy, average_time):
	result = 0
	divisor = 0

	not_racy = total_runs - racy

	for i in range(0, not_racy):
		result += math.comb(not_racy, i) * racy * average_time * (i + 1)


	for i in range(0, not_racy):
		divisor += math.comb(not_racy, i) * racy

	if divisor == 0:
		return float("inf")

	return result / divisor




if __name__ == "__main__":
	app = sys.argv[1]
	pmrace_results_dir = sys.argv[2] + os.sep
	hawkset_results_dir = sys.argv[3] + os.sep

	pmrace_racy_nr1, pmrace_racy_nr2, pmrace_total = get_pmrace_data(app, pmrace_results_dir)
	hawkset_racy_nr1, hawkset_racy_nr2, hawkset_total, hawkset_time = get_hawkset_data(app, hawkset_results_dir)

	assert pmrace_total == hawkset_total

	hawkset_avg_time = hawkset_time / hawkset_total

	ttr_pmrace_1 = avg_time_to_race(pmrace_total, pmrace_racy_nr1, 600)
	ttr_hawkset_1 = avg_time_to_race(hawkset_total, hawkset_racy_nr1, hawkset_avg_time)
	ttr_pmrace_2 = avg_time_to_race(pmrace_total, pmrace_racy_nr2, 600)
	ttr_hawkset_2 = avg_time_to_race(hawkset_total, hawkset_racy_nr2, hawkset_avg_time)

	print(f"-------------------------------------------------------------------------")
	print(f"         | Bug | Executions | Racy | Avg Time (s) | Avg Time to Race (s) ")
	print(f"-------------------------------------------------------------------------")
	print(f"  PMRace |     |            |{pmrace_racy_nr1: >5} |{600.0: >10.02f}    |{ttr_pmrace_1: >15.2f}           ")
	print(f"---------| #1  |            |--------------------------------------------")
	print(f" HawkSet |     |            |{hawkset_racy_nr1: >5} |{hawkset_avg_time: >10.02f}    |{ttr_hawkset_1: >15.2f}           ")
	print(f"---------------|     {hawkset_total:^3}    |--------------------------------------------")
	print(f"  PMRace |     |            |{pmrace_racy_nr2: >5} |{600.0: >10.02f}    |{ttr_pmrace_2: >15.2f}           ")
	print(f"---------| #2  |            |--------------------------------------------")
	print(f" HawkSet |     |            |{hawkset_racy_nr2: >5} |{hawkset_avg_time: >10.02f}    |{ttr_hawkset_2: >15.2f}           ")
	print(f"-------------------------------------------------------------------------")

	print("")

	print(f"Speedup: {ttr_pmrace_1 / ttr_hawkset_1:.2f}x  (bug #1)")
	print(f"Speedup: {ttr_pmrace_2 / ttr_hawkset_2:.2f}x  (bug #2)")
