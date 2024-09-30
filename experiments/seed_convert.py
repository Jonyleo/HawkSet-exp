import sys
import os
from glob import glob

def main():
	input_dir = sys.argv[1]
	output_dir = sys.argv[2]

	for seed in glob(input_dir + os.sep + "*"):
		with open(seed, "r") as f_seed:
			ops = f_seed.readlines()

		converted = []

		for op in ops:
			op = op.strip().split()
			
			if len(op) == 0:
				continue

			c = op[0]

			operands = list(str(int(x, 16)) for x in op[1:])

			op = c + ";" + ";".join(operands)

			converted.append(op + "\n")

		i = seed.rfind(os.sep)
		output =  output_dir + seed[i:]

		with open(output, "w") as f_workload:
			f_workload.writelines(converted)




main()