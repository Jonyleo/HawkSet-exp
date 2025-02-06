# id: [(new, app, store, load), ...]

bug_patterns = {

# Fast-Fair
1 : [
(False, "ffair", "btree.h:560", "btree.h:878"),
(False, "ffair", "btree.h:560", "btree.h:876"),
(False, "ffair", "btree.h:560", "btree.h:886")
],

2: [
(True, "ffair", "btree.h:571", "btree.h:878"),
(True, "ffair", "btree.h:571", "btree.h:876"),
(True, "ffair", "btree.h:571", "btree.h:886")
],

# P-CLHT

3: [
(False, "pclht", "clht_lb_res.c:793", "clht_lb_res.c:866"),
(False, "pclht", "clht_lb_res.c:793", "clht_lb_res.c:437"),
(False, "pclht", "clht_lb_res.c:793", "clht_lb_res.c:583"),
(False, "pclht", "clht_lb_res.c:793", "clht_lb_res.c:534"),
(False, "pclht", "clht_lb_res.c:793", "clht_gc.c:50"),
(False, "pclht", "clht_lb_res.c:793", "clht_gc.c:103"),
(False, "pclht", "clht_lb_res.c:793", "clht_gc.c:154"),
(False, "pclht", "clht_lb_res.c:793", "clht_gc.c:132"),
(False, "pclht", "clht_lb_res.c:793", "clht_gc.c:255")
],

# TurboHash

4: [(True, "turbohash", "turbo_hash_pmem_pmdk.h:2238", "turbo_hash_pmem_pmdk.h:2547"),],

# P-Masstree

5: [(None, "pmasstree", "masstree.h:868", "masstree.h:1958"),],

6: [(None, "pmasstree", "masstree.h:1435", "masstree.h:1958"),],

7: [(None, "pmasstree", "masstree.h:1473", "masstree.h:1953"),],

# P-ART

8: [
(None, "part", "N4.cpp:59", "N4.cpp:93"),
(None, "part", "N16.cpp:50", "N4.cpp:93"),
(None, "part", "N256.cpp:54", "N4.cpp:93"),
(None, "part", "N4.cpp:59", "N16.cpp:98"),
(None, "part", "N16.cpp:50", "N16.cpp:98"),
(None, "part", "N256.cpp:54", "N16.cpp:98"),
(None, "part", "N4.cpp:59", "N256.cpp:76"),
(None, "part", "N16.cpp:50", "N256.cpp:76"),
(None, "part", "N256.cpp:54", "N256.cpp:76")
],

9: [
(None, "part", "N4.cpp:104", "N4.cpp:93"),
(None, "part", "N4.cpp:104", "N16.cpp:98"),
(None, "part", "N16.cpp:113", "N4.cpp:93"),
(None, "part", "N16.cpp:113", "N16.cpp:98"),
],

# Memcached-pmem

10: [(False, "pmemcached", "memcached.c:4292", "memcached.c:2805"),],

11: [(False, "pmemcached", "memcached.c:4293", "memcached.c:2805"),],

12: [(False, "pmemcached", "items.c:423", "items.c:464"),],

13: [(False, "pmemcached", "slabs.c:549", "slabs.c:412"),],

14: [(False, "pmemcached", "items.c:1096", "memcached.c:2824"),],

15: [(False, "pmemcached", "items.c:627", "items.c:623"),],

# WIPE

16: [
(True, "wipe", "pointer_bentry.h:1771", "pointer_bentry.h:1606"),
(True, "wipe", "pointer_bentry.h:1779", "pointer_bentry.h:1606")
],

17: [
(True, "wipe", "pointer_bentry.h:1550", "pointer_bentry.h:1601"),
(True, "wipe", "pointer_bentry.h:1772", "pointer_bentry.h:1601")
],

18: [(True, "wipe", "letree.h:393", "letree.h:228"),],

# APEX

19: [
(True, "apex", "apex_nodes.h:3479", "apex_nodes.h:2915"),
(True, "apex", "apex_nodes.h:3798", "apex_nodes.h:2915"),
(True, "apex", "apex_nodes.h:3479", "apex_nodes.h:2933"),
(True, "apex", "apex_nodes.h:3798", "apex_nodes.h:2933")
],

20: [
(True, "apex", "apex_nodes.h:3480", "apex_nodes.h:962"),
(True, "apex", "apex_nodes.h:3606", "apex_nodes.h:962")
]

}


def test_bug(app, write_trace, read_trace, pattern):
	for bug in pattern:
		_, _, write, read = bug

		if write in write_trace and read in read_trace:
			return bug

	return False


def found_bug_pmrace(app, filename, pattern):
	with open(filename, "r") as f_race:
		line = f_race.readline()

		while line:
			if line.startswith("UWR"):
				write = f_race.readline()
				read = f_race.readline()

				if test_bug(app, write, read, bug_patterns[pattern]):
					return True

			line = f_race.readline()
	return False


def find_bug_hawkset(app, bugs, pattern, recursive=False):
	for bug in bugs:
		for write, _, reads in bugs:
			if recursive:
				write = "\n".join(write)
			else:
				write = write[0]

			for bug in bug_patterns[pattern]:
				_, _, w, r = bug
				if w not in write:
					continue

				for read in reads:
					if recursive:
						read = "\n".join(read)
					else:
						read = read[0]
					if r in read:
						return bug
						 
	return False


def found_bug_hawkset(app, bugs, pattern):
	return find_bug_hawkset(app, bugs, pattern) != False
