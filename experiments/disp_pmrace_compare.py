import os
import sys
import glob
from utils import *

from parse_races import parse_bugs

def test_bug(app, write, read):
	if app == "fast_fair" or True:
		return "src/btree.h:571" in write and (
			   "src/btree.h:876" in read or "src/btree.h:878" in read or "src/btree.h:886" in read
			)
	elif app == "pclht":
		return "clht_lb_res.c:804" in write and (
			   "src/clht_lb_res.c:877" in read or "src/clht_lb_res.c:717" in read or 
			   "src/clht_lb_res.c:373" in read or "src/clht_lb_res.c:431" in read or
			   "src/clht_lb_res.c:578" in read or "src/clht_lb_res.c:528" in read or 
			   "src/clht_gc.c:103" in read or "src/clht_gc.c:132" in read or 
			   "src/clht_gc.c:154" in read
			)


def found_bug_hawkset(app, filename):
	with open(filename, "r") as f_race:
		bugs = parse_bugs(f_race, None)

		for write, _, reads in bugs:

			for read in reads:
				if test_bug(app, write[0], read[0]):
					return True

	return False

import math

def calc_attr(n_runs_hawkset, n_races_found_by_hawkset, hawkset_time):
	e_execs = n_runs_hawkset - n_races_found_by_hawkset
	s_execs = n_races_found_by_hawkset
	t = hawkset_time / n_runs_hawkset

	attr = 0
	div = 0

	for i in range(0, e_execs + 1):
		attr += math.comb(e_execs, i) * s_execs * t * (i+1)
		div += math.comb(e_execs, i) * s_execs

	return attr/div


def get_vals(app, hawkset_dir):
	hawkset_time = 0
	n_runs_hawkset = 0

	for result in glob.glob(hawkset_dir + os.sep  + "*.info"):
		n_runs_hawkset += 1
		info = extract_info(result)

		hawkset_time += info["elapsed"]


	n_races_found_by_hawkset = 0
	for race in glob.glob(hawkset_dir + os.sep  + "*.log"):
		if found_bug_hawkset(app, race):
			n_races_found_by_hawkset += 1

	print(n_runs_hawkset, n_races_found_by_hawkset, hawkset_time, hawkset_dir)

	attr = calc_attr(n_runs_hawkset, n_races_found_by_hawkset, hawkset_time)

	#print(f"HawkSet's analysis time (per workload): {hawkset_time / n_runs_hawkset:.4f} s")
	#print(f"HawkSet's analysis time (total): {hawkset_time:.4f} s")
	#print(f"HawkSet's bug finding efficacy: {n_races_found_by_hawkset / n_runs_hawkset * 100:.2f}% ({n_races_found_by_hawkset} out of {n_runs_hawkset})")	
	#print(f"Avg time to detect race: {hawkset_time / (n_races_found_by_hawkset):.2f}")


	return attr, hawkset_time, n_races_found_by_hawkset

if __name__ == "__main__":
	app = sys.argv[1]
	hawkset_dir = sys.argv[2] 


	attr_avg = 0
	time_avg = 0
	races_found_avg = 0
	for i in range(2,11):
		attr, time, races = get_vals(app, hawkset_dir  + str(i))

		attr_avg += attr
		time_avg += time
		races_found_avg += races

	attr_avg /= 9
	time_avg /= 9
	races_found_avg //= 9


	print(attr_avg, time_avg, time_avg/240, races_found_avg, calc_attr(240,races_found_avg, time_avg))
