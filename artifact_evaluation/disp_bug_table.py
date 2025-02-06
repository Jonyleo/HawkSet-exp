import os
import sys
import glob
from parsing_utils import parse_all, parse_data, app_names
import math

from bugs import found_bug_pmrace, find_bug_hawkset, bug_patterns

last_app = ""

def display_bug_line(id, pattern):
	global last_app
	is_new, app, write, read = pattern

	if is_new is True:
		is_new = "✓"
	elif is_new is False:
		is_new = "x"
	else:
		is_new = "*"


	if last_app != app:
		last_app = app
		app = app_names[app]
		print("-"*(16+3+3+30+30))
	else:
		app = ""


	print(f"{app:16}|{id: >3}|{is_new: ^3}|{write: ^30}|{read: ^30}")

def display_bug_table(results_dir):
	bugs = parse_all(results_dir, None)

	print(f"{'Application':16}|{'#': ^3}|New|{'Store Access': ^30}|{'Load Access': ^30}")

	# 20 Bug patterns
	for i in range(1, 21):

		if i not in bug_patterns:
			continue

		app = bug_patterns[i][0][1]

		if app not in bugs:
			continue

		for bug in bugs[app]:

			if "irh0" in bug:
				continue

			b = find_bug_hawkset(app, bugs[app][bug], i, True)
			if b:
				display_bug_line(i, b)
				break


if __name__ == "__main__":
	hawkset_results_dir = sys.argv[1] + os.sep

	display_bug_table(hawkset_results_dir)