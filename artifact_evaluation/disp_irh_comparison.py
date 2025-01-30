import os
import sys
import glob
from parsing_utils import parse_all, parse_data, app_names, clean_all, start_limiters, end_limiters, get_parser
import math

from bugs import found_bug_pmrace, find_bug_hawkset, bug_patterns

from collections import defaultdict

last_app = ""

def display_line(app, after_irh, total_races):
	app = app_names[app]

	print(f"{app:16}|{'':14}|{after_irh: ^14}|{total_races: ^16}|")

def count_unique_races(races):
	unique_races = defaultdict(set)

	for write, _, reads in races:
		unique_races[write].update(reads)

	return len(unique_races)

def display_table(results_dir):
	args = get_parser().parse_args(
	[
		"input",
		"output",
		"--no_flush",
		"--single_trace",
		"--extra_clean",
		"--use_limiters"
	]
	)


	bugs = parse_all(results_dir, args)
	bugs = clean_all(bugs, start_limiters, end_limiters, args)

	print(f"{'':16}|{'Manual': ^14}|{'Automatic': ^31}|")
	print(f"{'Application':16}|{'MR': ^4}|{'BR': ^4}|{'FP': ^4}|{'After IRH': ^14}|{'Reported Races': ^16}|")

	for app in ["ffair", "turbohash", "pclht", "pmasstree", "part", "madfs-zipf_4k", "pmemcached", "wipe", "apex"]:
		if app not in bugs:
			continue

		for run in bugs[app]:
			if "100000-irh0" in run:
				irh0 = run
				break
		else:

			for run in bugs[app]:
				if "10000-irh0" in run:
					irh0 = run
					break

			else:

				for run in bugs[app]:
					if "1000-irh0" in run:
						irh0 = run
						break

		irh1 = irh0.replace("irh0", "irh1")

		irh0_data = count_unique_races(bugs[app][irh0])
		irh1_data = count_unique_races(bugs[app][irh1])

		display_line(app, irh1_data, irh0_data)


if __name__ == "__main__":
	hawkset_results_dir = sys.argv[1] + os.sep

	display_table(hawkset_results_dir)
