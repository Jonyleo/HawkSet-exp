import sys
import os
import math
import numpy  as np


import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter, StrMethodFormatter, LogLocator

import report
import parse

irh = 1
def bar_resource(x_data, runs, resource, x_axis_label="", y_axis_label="", title="", x_balance=1, y_balance=1, **kwargs):
	dataset = []
	width = 0.25
	multiplier = 0
	x = np.arange(len(runs))
	
	plt.rcParams['figure.constrained_layout.use'] = True

	for load,color in zip(x_data, ("red","green", "blue")):
		data = []
		error = []
		for program in sorted(runs):
			data.append(runs[program][irh][load][resource][0])
			error.append(runs[program][irh][load][resource][1])

		offset = width * multiplier
		rects = plt.bar(x+offset, data, width, label=load, yerr=error, capsize=3, ecolor="black",color=color)
		plt.bar_label(rects, padding=3, fmt="{:,.1f}")
		multiplier += 1


	labels = []
	for label in sorted(runs):
		if label in report.apps_names:
			labels.append(report.apps_names[label])
		else:
			labels.append(label)

	plt.xticks(x+width, labels)
	legend = plt.legend(**kwargs)
	plt.xlabel(x_axis_label)
	plt.ylabel(y_axis_label)
	plt.title(title)
	plt.ylim(0,256)

	#make_plot(x_data, dataset, zip(y_labels, colors, markers), x_axis_label, y_axis_label, title, x_balance, y_balance,**kwargs)

irh = 1
def make_plot(x_data, dataset, y_labels, x_axis_label="", y_axis_label="", title="applications", x_balance=1, y_balance=1, **kwargs):
	
	x_data = list(int((x+1000) / x_balance) for x in x_data)

	plots= []

	for data, metadata  in zip(dataset, y_labels):
		label,color,marker,linestyle = metadata
		y_data = list(((y[0] / y_balance) for y in data))
		error = list(y[1]  for y in data)
		if label in report.apps_names:
			label = report.apps_names[label]
		print(x_data, y_data)
		plots.append(plt.errorbar(x_data, y_data, capsize=3, elinewidth=0.75, capthick=0.75, ecolor="red", zorder=3, barsabove=True, yerr=error, label=label, marker=marker, linestyle=linestyle, linewidth=2, markersize=8, color=color)[0])

	plt.ylim(0)
	plt.xlim(0)
	modifier = ""
	if x_balance == 1000:
		modifier = "K"
	elif x_balance == 1000000:
		modifier = "M"
	elif x_balance == 1000000000:
		modifier = "G"
		

	plt.xticks(x_data, list(str(x) + modifier for x in x_data))


	if "ncol" in kwargs:
		del kwargs["ncol"]
	if "loc" in kwargs:
		del kwargs["loc"]

	leg1 = plt.legend(handles=plots[:4], ncol=4, loc="lower center",**kwargs)
	plt.gca().add_artist(leg1)
	leg2 = plt.legend(handles=plots[4:], ncol=len(plots)-4)

	leg2.remove()
	leg1._legend_box._children.append(leg2._legend_handle_box)
	leg1._legend_box.stale = True

	plt.xlabel(x_axis_label)
	plt.ylabel(y_axis_label)
	plt.title(title)

	return leg1

def plot_resource(x_data, runs, resource, x_axis_label="", y_axis_label="", title="", x_balance=1, y_balance=1, **kwargs):
	dataset = []
	y_labels = []
	#colors = ("red", "mediumturquoise", "blue", "green", "darkorange", "purple", "lime")
	#colors = ("#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0")

	colors = ("#666666", "#999999", "#000000", "#666666", "#000000", "#666666", "#000000")
	line = ("dashed", "solid", "dashed", "dashdot", "solid", "dashdot", "dotted")
	markers = ("o", "v", "s", "o", "v", "s", "o")

	for program in sorted(runs):
		y_data = []
		y_labels.append(program)
		for load in x_data:
			y_data.append(runs[program][irh][load][resource])
		dataset.append(y_data)

	return make_plot(x_data, dataset, zip(y_labels, colors, markers, line), x_axis_label, y_axis_label, title, x_balance, y_balance, **kwargs)


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
					if prop == "elapsed" and irh == 1:
						print(app, irh, load, stdev)

					result[app][irh][load][prop] = (mean, stdev)

	return result



def do_bugs(report_folder, output_folder):
	bugs_per_run = []
	for run in os.listdir(report_folder):
		_, _, i = run.rpartition("_")

		bugs = parse.parse_all(report_folder + os.sep + run)

		bugs_per_run.append(bugs)

	bugs = merge_bugs(bugs_per_run)

	parse.output_programs(output_folder, bugs)

	bugs = parse.clean_all(bugs, parse.program_limiters)
	parse.output_programs(output_folder+"-clean", bugs)


	parse.output_csv(output_folder+"-csv", bugs)

def fraction_formater(val, _):
		if val >= 1:
			return str(int(val))

		else:
			if val == 0.5:
				return "½"
			elif val == 0.25:
				return "¼"
			elif val == 0.125:
				return "⅛"
			elif val == 0.0625:
				return "¹⁄₁₆"

		return "Nan"

def do_data(report_folder, output_folder):
	data_per_run = []
	for run in os.listdir(report_folder):
		_, _, i = run.rpartition("_")

		data = report.extract_runs(report_folder + os.sep + run)

		if "Montage-Graph" in data:
			data["MontageGraph"] = data["MontageGraph-Custom"]
			del data["MontageGraph-Custom"]


		data_per_run.append(data)

	data = merge_data(data_per_run)

	def format_axes():
		plt.xscale("log", base=2)
		plt.yscale("log", base=2)
		plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
		plt.gca().yaxis.set_minor_formatter(FuncFormatter(lambda x, pos: " "))
		plt.gca().yaxis.set_minor_locator(LogLocator(base=2, subs="all", numticks=1000))



	format_axes()
	legend = plot_resource([1000, 10000, 100000], data, "elapsed", "Operations (#)", "Elapsed time (s)", "", 1000, 1, \
		ncol=7, bbox_to_anchor=(0.5, 1.3), loc='upper center', fontsize="12", frameon=False)
	legend.remove()
	report.set_aspect_ratio(0.5)

	plt.savefig("time-elapsed.pdf", bbox_inches='tight')
	plt.clf()

	# format_axes()
	# plt.gca().yaxis.set_major_formatter(FuncFormatter(fraction_formater))
	# legend = plot_resource([1000, 10000, 100000], data, "pm stores", "Operations (#)", "PM Store Instructions (M)", "", 1000, 1000000, \
	# 	ncol=4, bbox_to_anchor=(0.5, 1.3), loc='upper center', fontsize="12", frameon=False)

	# fig = legend.figure
	# fig.canvas.draw()
	# bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
	# fig.savefig("legend-1.pdf", dpi="figure", bbox_inches=bbox)
	
	# legend.remove()

	# report.set_aspect_ratio(0.5)

	# plt.savefig("pm-stores.pdf", bbox_inches='tight')
	# plt.clf()

	

	# format_axes()
	# plt.gca().yaxis.set_major_formatter(FuncFormatter(fraction_formater))
	# legend = plot_resource([1000, 10000, 100000], data, "pm loads", "Operations (#)", "PM Load Instructions (M)", "", 1000, 1000000, \
	# 	ncol=7, bbox_to_anchor=(0.5, 1.3), loc='upper center', fontsize="12", frameon=False)
	# legend.remove()
	# report.set_aspect_ratio(0.5)
	# plt.savefig("pm-loads.pdf", bbox_inches='tight')
	# plt.clf()

	# format_axes()
	# legend = plot_resource([1000, 10000, 100000], data, "mem", "Operations (#)", "Peak Memory Usage (GB)", "", 1000, 1000000, \
	# 	ncol=7, bbox_to_anchor=(0.5, 1.3), loc='upper center', fontsize="12", frameon=False)
	# legend.remove()
	# report.set_aspect_ratio(0.5)
	# plt.savefig("mem-used.pdf", bbox_inches='tight')
	# plt.clf()

if __name__ == "__main__":
	report_folder=sys.argv[1]
	output_folder=sys.argv[2]
	
	#do_bugs(report_folder, output_folder)
	do_data(report_folder, output_folder)



	
