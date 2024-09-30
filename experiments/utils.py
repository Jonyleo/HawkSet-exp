from datetime import datetime
from parse_races import parse_bugs

def extract_info(file_name):
	res = {

	}
	instrs = [ 
		"pm stores",
		"pm nt stores",
		"pm loads",
		"flushes",
		"fences",
		"rmw"
	]

	with open(file_name) as f_in:
		for line in f_in.readlines():
			if "Maximum resident" in line:
				i = line.find(": ")
				res["mem"] = int(line[i+2:])

			elif "m:ss" in line:
				i = line.find(": ")
				elapsed = line[i+2:-1]
				try:
					t = datetime.strptime(elapsed, "%M:%S.%f")
				except:
					t = datetime.strptime(elapsed, "%H:%M:%S")

				res["elapsed"] = (t-datetime(1900,1,1)).total_seconds()


			elif "User time" in line:
				i = line.find(": ")
				res["analysis"] = float(line[i+2: ])
				
			else:
				for instr in instrs:
					if instr in line:
						i = line.find(": ")
						res[instr] = int(line[i+2: ])
						break


	if "pm stores" in res:
		res["pm stores"] += res["pm nt stores"]

	return res

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

def found_bug_pmrace(app, filename):
	with open(filename, "r") as f_race:
		line = f_race.readline()

		while line:
			if line.startswith("UWR"):
				write = f_race.readline()
				read = f_race.readline()

				if test_bug(app, write, read):
					return True

			line = f_race.readline()
	return False


def found_bug_hawkset(app, filename):
	with open(filename, "r") as f_race:
		bugs = parse_bugs(f_race)
		
		for write, _, reads in bugs:

			for read in reads:
				if test_bug(app, write[0], read[0]):
					return True
						
	return False
