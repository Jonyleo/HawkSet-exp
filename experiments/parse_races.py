import sys
import os
import glob
from collections import defaultdict
import csv

def trace_to_string(trace):
	return "".join([x.replace("\n", "") for x in trace])

def bug_to_string(bug, no_flush):
	write, flush, reads = bug

	string = ""

	if no_flush:
		return "WRITE:\n" + trace_to_string(write) + "\n" + \
			   "READS:\n" + "---\n".join(trace_to_string(r) for r in reads)

	else:
		return "WRITE:\n" + trace_to_string(write) + "\n" + \
			   "FLUSH:\n" + trace_to_string(flush) + "\n" + \
			   "READS:\n" + "---\n".join(trace_to_string(r) for r in reads)

def bug_to_csv(bug, no_flush):
	write, flush, reads = bug

	string = ""

	if no_flush:
		return [trace_to_string(write), "\n".join(trace_to_string(r) for r in reads)]
	else:
		return [trace_to_string(write), trace_to_string(flush), "\n".join(trace_to_string(r) for r in reads)]

def output_bugs(path, bugs, no_flush, to_csv):
	unrepeated_bugs = defaultdict(set)

	for write, flush, reads in bugs:
		if no_flush:
			unrepeated_bugs[(write, "")].update(reads)
		else:
			unrepeated_bugs[(write, flush)].update(reads)

	bugs = [(*key, val) for key, val in unrepeated_bugs.items()]

	if to_csv:
		with open(path, "w", newline="") as f_out:
			writer = csv.writer(f_out, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)

			if no_flush:
				writer.writerow(["WRITE", "READS"])
			else:
				writer.writerow(["WRITE", "FLUSH", "READS"])

			for b in bugs:
				writer.writerow(bug_to_csv(b, no_flush))

	else:
		with open(path, "w") as f_out:
			print("\n".join(bug_to_string(b, no_flush) for b in bugs), file=f_out)

def eot(line):
	return line.isspace() or line == "" 

def parse_trace(file, ending=""):
	trace = []

	while True:
		line = file.readline()
		if line.strip() == ending or eot(line):
			break

		trace.append(line)
	return tuple(trace), line

def parse_bug(file):
	line = file.readline() # Ignore "PM address written in:"

	if eot(line):
		return None,None,None

	write,_ = parse_trace(file)

	file.readline() # Ignore "flushed in:"
	flush,_ = parse_trace(file)

	file.readline() # Ignore "can be acessed concurrently in:"
	reads= []

	while True:
		read, line = parse_trace(file, "---")
		reads.append(read)

		if eot(line):
			break

	return write, flush, reads


def parse_bugs(file):
	bugs = []

	while True:
		write, flush, read = parse_bug(file)

		if write is None:
			return bugs

		
		bugs.append((write,flush,read))
		
def parse_program(program_path):
	files = glob.glob(program_path + os.sep + "*.log")

	res = []

	for file in files:
		with open(file) as f_in:
			res.append((file, parse_bugs(f_in)))

	return dict(res)

def clean_trace(trace, start_limiter, end_limiter, single_trace):
	assert(start_limiter != "")
	for i, line in enumerate(trace[-1::-1]):
		i = len(trace) - i - 1

		if start_limiter in line:
			trace = trace[0:i+1]
			break

	for i, line in enumerate(trace):
		if end_limiter in line:
			trace = trace[i:]
			break

	if single_trace:
		return trace[0]

	return trace

def clean_bug(bug, start_limiter, end_limiter, single_trace):
	write, flush, reads = bug

	write = clean_trace(write, start_limiter, end_limiter, single_trace)
	flush = clean_trace(flush, start_limiter, end_limiter, single_trace)

	cleaned_reads = []

	for i, read in enumerate(reads):
		cleaned_reads.append(clean_trace(read, start_limiter, end_limiter, single_trace))

	return write, flush, cleaned_reads

def clean_bugs(bugs, start_limiter, end_limiter, single_trace):
	cleaned_bugs = []
	for bug in bugs:
		cleaned_bugs.append(clean_bug(bug, start_limiter, end_limiter, single_trace))

	return cleaned_bugs

def clean_program(program, start_limiter, end_limiter, single_trace):
	cleaned_program = {}
	
	for file, bugs in program.items():
		cleaned_program[file] = clean_bugs(bugs, start_limiter, end_limiter, single_trace)

	return cleaned_program


def parse_all(path):
	programs = os.listdir(path)

	return dict((p,parse_program(path + os.sep + p)) for p in programs)

def clean_all(programs, start_limiters, end_limiters, single_trace):
	cleaned_programs = {}


	for program_name, program_bugs in programs.items():
		cleaned_programs[program_name] = clean_program(program_bugs, start_limiters[program_name], end_limiters[program_name], single_trace)

	return cleaned_programs

start_limiters = {
	"ffair" : "/root/FAST_FAIR/concurrent_pmdk/src/btree.h",
	"pclht" : "/root/RECIPE/P-CLHT/src/clht_lb_res.c",
	"turbohash": "/root/TurboHash/src/turbo/turbo_hash_pmem_pmdk.h",
	"pmemkv-cmap" : "/usr/local/include/libpmemkv.hpp",
	"pmemkv-csmap" : "/usr/local/include/libpmemkv.hpp",
	"pmemkv-robinhood" : "/usr/local/include/libpmemkv.hpp",
	"montage-MontageGraph-Custom" : "MontageGraph.hpp",
	"montage-MontageQueue" : "MontageQueue.hpp",
	"montage-MontageHashTable" : "MontageHashTable.hpp",
	"madfs-zipf_4k": "/root/MadFS/src/lib",
	"part": "Tree.cpp",
	"phot": "HOTRowex.hpp",
	"pmasstree": "masstree.h"
}

end_limiters = {
	"ffair" : "btree.h",
	"pclht" : "",
	"turbohash": "/root/TurboHash/src/turbo/turbo_hash_pmem_pmdk.h",
	"pmemkv-cmap" : "",
	"pmemkv-csmap" : "",
	"pmemkv-robinhood" : "",
	"montage-MontageGraph-Custom" : "",
	"montage-MontageQueue" : "",
	"montage-MontageHashTable" : "",
	"madfs-zipf_4k": "root/MadFS/src/block",
	"part": "(/root/durinn/third_party/RECIPE/P-ART",
	"phot": "(/root/durinn/third_party/RECIPE/P-HOT",
	"pmasstree": "masstree.h"
}


def output_programs(path, programs, no_flush, to_csv):
	files = []
	for program, program_bugs in programs.items():
		
		for file, bugs in program_bugs.items():
			file = path + os.sep + program + "-" + file.rpartition(os.sep)[2]

			if to_csv:
				file = file.replace(".log", ".csv")
			
			files.append(file)


			output_bugs(file, bugs, no_flush, to_csv)

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

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('input', help='input path')
	parser.add_argument('output', help='output path')
	parser.add_argument('--no_flush', help='ignore flush trace', action="store_true")
	parser.add_argument('--single_trace', help='use sigle trace level', action="store_true")
	parser.add_argument('--csv', help='output to csv format', action="store_true")
	args = parser.parse_args()

	input_path = args.input
	output_path = args.output
	no_flush = args.no_flush
	single_trace = args.single_trace
	to_csv = args.csv

	if not os.path.exists(output_path):
		os.mkdir(output_path)

	if not os.path.exists(input_path):
		print("Invalid input path")
		exit(-1)

	kv = parse_all(input_path)

	kv = clean_all(kv, start_limiters, end_limiters, single_trace)
	output_programs(output_path, kv, no_flush, to_csv)
