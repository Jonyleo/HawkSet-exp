import os
import sys
import glob
from parse_races import parse_bugs
from utils import *

if __name__ == "__main__":
	app = sys.argv[1]
	results_dir = sys.argv[2] + os.sep + app

	n_ops = 0

	all_seeds = set()
	seeds_with_races = set()
	"/home/joliveira/Exp-HawkSet-exp/pmrace_results/seeds/pclht/000002/000002/***parsed"

	print(results_dir + os.sep + "*" + os.sep + "*" + os.sep +  "*---race.csv.parsed")
	for race in glob.glob(results_dir + os.sep + "*" + os.sep + "*" + os.sep +  "*---race.csv.parsed"):
		seed = race.split(os.sep)[-2]

		all_seeds.add(seed)

		if seed in seeds_with_races:
			continue

		if found_bug_pmrace(app, race):
			seeds_with_races.add(seed)

	print(f"Seeds executed: {len(all_seeds)}")
	print(f"PMRace found races in {len(seeds_with_races)} seeds within 10 mins")

	