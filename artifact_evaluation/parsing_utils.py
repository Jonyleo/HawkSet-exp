import os
import glob
from collections import defaultdict
import csv
import re
import math

from datetime import datetime


def trace_to_string(trace):
	return "\n".join([x.replace("\n", "") for x in trace])

def bug_to_string(bug, args):

	write, flush, read = bug

	if args.cluster == "NONE":
		read = trace_to_string(read)
	else:
		read = "\n---\n".join(trace_to_string(r) for r in read)


	if args.csv:
		if args.no_flush:
			return [trace_to_string(write), read]
		else:
			return [trace_to_string(write), trace_to_string(flush), read]

	else:
		if args.no_flush:
			return args.first_header + ":\n" + trace_to_string(write) + "\n" + \
				   args.second_header + ":\n" + read

		else:
			return args.first_header + ":\n" + trace_to_string(write) + "\n" + \
				   "FLUSH:\n" + trace_to_string(flush) + "\n" + \
				   args.second_header + ":\n" + read

def output_bugs(path, bugs, args):

	unrepeated_bugs = defaultdict(set)

	if args.cluster == "READ":
		if not args.no_flush:
			print("Cannot cluster by read with flush")
			exit(-1)

		for write, _, reads in bugs:
			for read in reads:
				unrepeated_bugs[(read, "")].update(set((write,)))

		bugs = [(*key, val) for key, val in unrepeated_bugs.items()]

	elif args.cluster == "WRITE":
		for write, flush, reads in bugs:
			if args.no_flush:
				unrepeated_bugs[(write, "")].update(reads)
			else:
				unrepeated_bugs[(write, flush)].update(reads)
		
		bugs = [(*key, val) for key, val in unrepeated_bugs.items()]

	else:
		for write, flush, reads in bugs:
			for read in reads:
				if args.no_flush:
					unrepeated_bugs[(write, "", read)] = set()
				else:
					unrepeated_bugs[(write, flush, read)] = set()

		bugs = [key for key, val in unrepeated_bugs.items()]
	

	if args.print_info:
		print(path[path.find("/")+1:path.rfind(".")], ": ", len(unrepeated_bugs))

	if args.cluster == "READ":
		args.first_header = "READ"
		args.second_header = "WRITES"
	elif args.cluster == "WRITE":
		args.first_header = "WRITE"
		args.second_header = "READS"
	elif args.cluster == "NONE":
		args.first_header = "WRITE"
		args.second_header = "READ"


	if "/dev/null" in path:
		return

	if args.csv:
		with open(path, "w", newline="") as f_out:
			writer = csv.writer(f_out, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)

			if args.no_flush:
				writer.writerow([args.first_header, args.second_header])
			else:
				writer.writerow([args.first_header, "FLUSH", args.second_header])
			
			for b in bugs:
				assert(len(b[2]) != 0)
				writer.writerow(bug_to_string(b, args))

	else:
		with open(path, "w") as f_out:
			print("\n\n".join(bug_to_string(b, args) for b in bugs), file=f_out)

def eot(line):
	return line.isspace() or line == "" 

def parse_trace(file, args, ending=""):
	trace = []

	while True:
		line = file.readline()
		if line.strip() == ending or eot(line):
			break

		trace.append(line)
	return tuple(trace), line

def parse_bug(file, args):
	line = file.readline() # Ignore "PM address written in:"

	if eot(line):
		return None,None,None

	write,_ = parse_trace(file, args)

	file.readline() # Ignore "flushed in:"
	flush,_ = parse_trace(file, args)

	file.readline() # Ignore "can be acessed concurrently in:"
	reads= []

	while True:
		read, line = parse_trace(file, args, "---")
		reads.append(read)

		if eot(line):
			break

	return write, flush, reads


def parse_bugs(file, args):
	bugs = []

	while True:
		write, flush, read = parse_bug(file, args)

		if write is None:
			return bugs

		
		bugs.append((write,flush,read))
		
def parse_program(program_path, args):
	files = glob.glob(program_path + os.sep + "*.log")

	res = []

	for file in files:
		with open(file) as f_in:
			res.append((file, parse_bugs(f_in, args)))

	return dict(res)

def clean_trace(trace, start_limiter, end_limiter, args):
	assert(start_limiter != "")

	if args.extra_clean:
		trace = tuple(re.sub("\+0x[0-9a-f]+", "", x) for x in trace)
		trace = tuple(re.sub(" at [^\(]+", " ", x) for x in trace)

	if not args.use_limiters:
		if args.single_trace:
			return (trace[0],)
		return trace

	for i, line in enumerate(trace[-1::-1]):
		i = len(trace) - i - 1

		if start_limiter in line:
			trace = trace[0:i+1]
			break

	for i, line in enumerate(trace):
		if end_limiter in line:
			trace = trace[i:]
			break

	if args.single_trace:
		return (trace[0],)

	return trace

def clean_bug(bug, start_limiter, end_limiter, args):
	write, flush, reads = bug

	write = clean_trace(write, start_limiter, end_limiter, args)
	flush = clean_trace(flush, start_limiter, end_limiter, args)

	cleaned_reads = []

	for i, read in enumerate(reads):
		cleaned_reads.append(clean_trace(read, start_limiter, end_limiter, args))

	return write, flush, cleaned_reads

def clean_bugs(bugs, start_limiter, end_limiter, args):
	cleaned_bugs = []
	for bug in bugs:
		cleaned_bugs.append(clean_bug(bug, start_limiter, end_limiter, args))

	return cleaned_bugs

def clean_program(program, start_limiter, end_limiter, args):
	cleaned_program = {}
	
	for file, bugs in program.items():
		cleaned_program[file] = clean_bugs(bugs, start_limiter, end_limiter, args)

	return cleaned_program



def parse_run(path, args):
	programs = os.listdir(path)

	return dict((p,parse_program(path + os.sep + p, args)) for p in programs)

def merge_bugs(bugs_per_run):
	result = {}

	for bugs in bugs_per_run:
		for app in bugs:
			if app not in result:
				result[app] = {}
			
			for file in bugs[app]:
				_, _, file_s = file.rpartition(os.sep)

				if file_s not in result[app]:
					result[app][file_s] = {}

				for write, flush, reads in bugs[app][file]:
					if (write, flush) not in result[app][file_s]:
						result[app][file_s][(write, flush)] = set(reads)
					else:
						result[app][file_s][(write, flush)].update(reads)


	for app in result:
		for file in result[app]:
			bugs = []
			for (write,flush), reads in result[app][file].items():
				bugs.append([write, flush, reads])
			result[app][file] = bugs

	return result


def parse_all(path, args):
	if "run_" not in os.listdir(path)[0]:
		return parse_run(path, args)

	bugs = []

	for run in os.listdir(path):
		run_path = path + os.sep + run
		bugs.append(parse_run(run_path, args))


	return merge_bugs(bugs)


def clean_all(programs, start_limiters, end_limiters, args):
	cleaned_programs = {}

	for program_name, program_bugs in programs.items():
		cleaned_programs[program_name] = clean_program(program_bugs, start_limiters[program_name], end_limiters[program_name], args)

	return cleaned_programs

start_limiters = {
	"ffair" : "/root/FAST_FAIR/concurrent_pmdk/src/btree.h",
	"pclht" : "/root/RECIPE/P-CLHT/src/clht_lb_res.c",
	"turbohash": "/root/TurboHash/src/turbo/turbo_hash_pmem_pmdk.h",
	"madfs-zipf_4k": "/root/MadFS/src/lib",
	"part": "Tree.cpp",
	"phot": "HOTRowex.hpp",
	"pmasstree": "masstree.h",
	"pmemcached": "/root/memcached-pmem",
	"wipe": "/root/WIPE/test/",
	"apex": "/root/apex/src/benchmark/../core"
}

end_limiters = {
	"ffair" : "btree.h",
	"pclht" : "/root/RECIPE/P-CLHT/src",
	"turbohash": "/root/TurboHash/src/turbo/turbo_hash_pmem_pmdk.h",
	"madfs-zipf_4k": "root/MadFS/src/block",
	"part": "(/root/durinn/third_party/RECIPE/P-ART",
	"phot": "(/root/durinn/third_party/RECIPE/P-HOT",
	"pmasstree": "masstree.h",
	"pmemcached": "/root/memcached-pmem",
	"wipe": "/root/WIPE/test/",
	"apex": "/root/apex/src/benchmark/../core"
}


def output_programs(path, programs, args):

	files = []
	for program, program_bugs in programs.items():
		for file, bugs in program_bugs.items():
			file = path + os.sep + program + "-" + file.rpartition(os.sep)[2]

			if args.csv:
				file = file.replace(".log", ".csv")
			
			files.append(file)


			output_bugs(file, bugs, args)

	if "/dev/null" in path:
		return
		
	import zipfile

	with zipfile.ZipFile(path + os.sep + "results.zip", "w") as f_zip:
		for file in files:
			f_zip.write(file, compress_type=zipfile.ZIP_DEFLATED, arcname=file[file.rfind(os.sep):])



def split_montage(program_bugs):
	program = {}


	for limiter in montage_limiters:
		program[limiter] = {}

	for file, bugs  in program_bugs.items():
		for limiter in montage_limiters:
			if limiter in file:
				program[limiter][file] = bugs

	return program


app_names = {
	"ffair" : "Fast-Fair",
	"fast_fair" : "Fast-Fair",
	"pclht" : "P-CLHT",
	"turbohash": "TurboHash",
	"madfs-zipf_4k": "MadFS",
	"part": "P-ART",
	"phot": "P-HOT",
	"pmasstree": "P-Masstree",
	"pmemcached": "Memcached-pmem",
	"wipe": "WIPE",
	"apex": "APEX"
}

def extract_run(file_name):
	folder, _, file_name = file_name.rpartition(os.sep)
	_, _, program = folder.rpartition(os.sep)
	run , _, _ = file_name.rpartition(".")
	load, _, irh = run.partition("-irh")

	return program, irh, load

def extract_info(file_name):
	res = {

	}
	instrs = [ 
		"pm stores:",
		"pm nt stores:",
		"pm loads:",
		"flushes:",
		"fences:",
		"rmw:",
		"stores:",
		"loads:"
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
						res[instr[:-1]] = int(line[i+2: ])
						break


	if "pm stores" in res:
		res["pm stores"] += res["pm nt stores"]

	return res

def extract_runs(report_folder):
	files = glob.glob(report_folder + "/*/*.info")

	runs = {}

	for file in files:
		program, irh, load = extract_run(file)

		irh = int(irh)
		try:
			load = int(load)
		except:
			pass


		info = extract_info(file)

		log = file.rpartition(".")[0] + ".log"
		if os.path.exists(log):
			info["log"] = log

		if program not in runs:
			runs[program] = {}
		if irh not in runs[program]:
			runs[program][irh] = {}
		if load not in runs[program][irh]:
			runs[program][irh][load] = info

	return runs

def merge_data(data_per_run):
	result = {}

	for bugs in data_per_run:
		for app in bugs:
			if app not in result:
				result[app] = {}
			
			for irh in bugs[app]:
				if irh not in result[app]:
					result[app][irh] = {}

				for load in bugs[app][irh]:
					if load not in result[app][irh]:
						result[app][irh][load] = {}

					for prop in bugs[app][irh][load]:
						if prop == "log":
							continue
						if prop not in result[app][irh][load]:
							result[app][irh][load][prop] = []

						result[app][irh][load][prop].append(bugs[app][irh][load][prop])


	for app in result:
		for irh in result[app]:
			for load in result[app][irh]:
				for prop in result[app][irh][load]:
					lst = result[app][irh][load][prop]

					total = sum(lst)
					mean = total/len(lst)
					stdev = math.sqrt(sum((x - mean)**2 for x in lst) / len(lst))
					
					result[app][irh][load][prop] = (mean, stdev)

	return result

def parse_data(input_path, args):
	if "run_" not in os.listdir(input_path)[0]:
		return merge_data([extract_runs(input_path)])

	data_per_run = []
	for run in os.listdir(input_path):
		_, _, i = run.rpartition("_")

		data = extract_runs(input_path + os.sep + run)

		data_per_run.append(data)

	return merge_data(data_per_run)


def get_parser():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('input', help='input path')
	parser.add_argument('output', help='output path')
	parser.add_argument('--no_flush', help='ignore flush trace', action="store_true")
	parser.add_argument('--single_trace', help='use sigle trace level', action="store_true")
	parser.add_argument('--csv', help='output to csv format', action="store_true", default=False)
	parser.add_argument('--cluster', help='cluster reports by read', choices=["READ", "WRITE", "NONE"], default="WRITE")
	parser.add_argument('--print_info', help='print some info', action="store_true")
	parser.add_argument('--extra_clean', help='remove semi-useless data from backtraces', action="store_true")
	parser.add_argument('--use_limiters', help='remove specific lines from traces', action="store_true")

	return parser


if __name__ == "__main__":

	args = get_parser().parse_args()

	input_path = args.input
	output_path = args.output

	if not os.path.exists(output_path):
		os.mkdir(output_path)

	if not os.path.exists(input_path):
		print("Invalid input path")
		exit(-1)

		
	bugs = parse_all(input_path, args)
	bugs = clean_all(bugs, start_limiters, end_limiters, args)

	output_programs(output_path, bugs, args)
