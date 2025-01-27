import os
import sys
import glob
from parsing_utils import parse_all, parse_data
import math

from bugs import found_bug_pmrace, found_bug_hawkset

def get_pmrace_data(app, results_dir):
	all_seeds = set()
	seeds_with_races_nr1 = set()
	seeds_with_races_nr2 = set()

	for race in glob.glob(results_dir + os.sep + "*" + os.sep + "*" + os.sep +  "*---race.csv.parsed"):
		seed = race.split(os.sep)[-2]
		all_seeds.add(seed)

		if seed in seeds_with_races_nr1 and seed in seeds_with_races_nr2:
			continue

		if found_bug_pmrace(app, race, 1):
			seeds_with_races_nr1.add(seed)

		if found_bug_pmrace(app, race, 2):
			seeds_with_races_nr2.add(seed)

	return len(seeds_with_races_nr1), len(seeds_with_races_nr2), len(all_seeds)

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
	pmrace_results_dir = sys.argv[2] + os.sep + app
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
	print(f"---------------|     {hawkset_total:03}    |--------------------------------------------")
	print(f"  PMRace |     |            |{pmrace_racy_nr2: >5} |{600.0: >10.02f}    |{ttr_pmrace_2: >15.2f}           ")
	print(f"---------| #2  |            |--------------------------------------------")
	print(f" HawkSet |     |            |{hawkset_racy_nr2: >5} |{hawkset_avg_time: >10.02f}    |{ttr_hawkset_2: >15.2f}           ")
	print(f"-------------------------------------------------------------------------")

	print("")

	print(f"Speedup: {ttr_pmrace_1 / ttr_hawkset_1:.2f}x  (bug #1)")
	print(f"Speedup: {ttr_pmrace_2 / ttr_hawkset_2:.2f}x  (bug #2)")