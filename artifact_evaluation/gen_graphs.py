import sys
import os

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter, StrMethodFormatter, LogLocator

import numpy as np

from parsing_utils import parse_data, app_names

def make_plot(x_data, dataset, y_labels, x_axis_label="", y_axis_label="", title="applications", x_balance=1, y_balance=1, **kwargs):
	
	x_data = list(int((x+1000) / x_balance) for x in x_data)

	plots= []

	for data, metadata  in zip(dataset, y_labels):
		label,color,marker,linestyle = metadata
		y_data = list(((y[0] / y_balance) for y in data))
		error = list(y[1]  for y in data)
		if label in app_names:
			label = app_names[label]

		if("P-ART" in label):
			x_data_ = x_data[0:1]
		else:
			x_data_ = x_data
		plots.append(plt.plot(x_data_, y_data, label=label, marker=marker, linestyle=linestyle, linewidth=2, markersize=6, color=color)[0])

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

	if(len(plots) == 1):
		leg1 = plt.legend(handles=plots, ncol=1, loc="lower center",**kwargs)
		plt.gca().add_artist(leg1)

	else:
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


	colors = ("#000000", "#333333", "#666666", "#999999", "#000000", "#333333", "#666666", "#999999", "#000000")
	line = ("dashed", "solid", "dotted", "solid", "dotted", "dashed", "dotted", "dashed", "solid")
	markers = ("o", "v", "P", "v", "o", "v", "v", "P", "o")

	for program in sorted(runs):
		y_data = []
		y_labels.append(program)
		for load in x_data:
			y_data_program = runs[program][1]

			if load in y_data_program:
				y_data.append(y_data_program[load][resource])

		dataset.append(y_data)

	return make_plot(x_data, dataset, zip(y_labels, colors, markers, line), x_axis_label, y_axis_label, title, x_balance, y_balance, **kwargs)

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

def set_aspect_ratio(ratio, xscale ="log", yscale="log"):
	x_left, x_right = plt.gca().get_xlim()
	y_low, y_high = plt.gca().get_ylim()

	if xscale == "log":
		x_right = np.log2(x_right)
		x_left = np.log2(x_left)

	if yscale == "log":
		y_high = np.log2(y_high)
		y_low = np.log2(y_low)

	aspect = abs((x_right- x_left)/(y_high- y_low)) * ratio

	plt.gca().set_aspect(aspect)

def plot_data(output_path, args):
	def format_axes():
		plt.xscale("log", base=2)
		plt.yscale("log", base=2)
		plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
		plt.gca().yaxis.set_minor_formatter(FuncFormatter(lambda x, pos: " "))
		plt.gca().yaxis.set_minor_locator(LogLocator(base=2, subs="all", numticks=1000))

	format_axes()
	plt.gca().yaxis.set_major_formatter(FuncFormatter(fraction_formater))
	legend = plot_resource([1000, 10000, 100000], data, "elapsed", "Operations (#)", "Elapsed time (s)", "", 1000, 1, \
		ncol=7, bbox_to_anchor=(0.5, 1.3), loc='upper center', fontsize="12", frameon=False)
	legend.remove()
	set_aspect_ratio(0.5)

	plt.savefig(output_path + os.sep + "time-elapsed.pdf", bbox_inches='tight')
	plt.clf()

	format_axes()
	plt.gca().yaxis.set_major_formatter(FuncFormatter(fraction_formater))
	legend = plot_resource([1000, 10000, 100000], data, "pm stores", "Operations (#)", "PM Store Instructions (M)", "", 1000, 1000000, \
		ncol=4, bbox_to_anchor=(0.5, 1.3), loc='upper center', fontsize="12", frameon=False)

	fig = legend.figure
	fig.canvas.draw()
	bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
	fig.savefig(output_path + os.sep + "legend-1.pdf", dpi="figure", bbox_inches=bbox)
	
	legend.remove()

	set_aspect_ratio(0.5)

	plt.savefig(output_path + os.sep + "pm-stores.pdf", bbox_inches='tight')
	plt.clf()

	format_axes()
	plt.gca().yaxis.set_major_formatter(FuncFormatter(fraction_formater))
	legend = plot_resource([1000, 10000, 100000], data, "pm loads", "Operations (#)", "PM Load Instructions (M)", "", 1000, 1000000, \
		ncol=7, bbox_to_anchor=(0.5, 1.3), loc='upper center', fontsize="12", frameon=False)
	legend.remove()
	set_aspect_ratio(0.5)
	plt.savefig(output_path + os.sep + "pm-loads.pdf", bbox_inches='tight')
	plt.clf()

	format_axes()
	plt.gca().yaxis.set_major_formatter(FuncFormatter(fraction_formater))
	legend = plot_resource([1000, 10000, 100000], data, "mem", "Operations (#)", "Peak Memory Usage (GB)", "", 1000, 1000000, \
		ncol=7, bbox_to_anchor=(0.5, 1.3), loc='upper center', fontsize="12", frameon=False)
	legend.remove()
	set_aspect_ratio(0.5)
	plt.savefig(output_path + os.sep + "mem-used.pdf", bbox_inches='tight')
	plt.clf()


if __name__ == "__main__":
	input_path = sys.argv[1]
	output_path = sys.argv[2]

	if not os.path.exists(output_path):
		os.mkdir(output_path)

	if not os.path.exists(input_path):
		print("Invalid input path")
		exit(-1)

	import warnings

	warnings.filterwarnings("ignore", message="Attempt to set non-positive .lim on a log-scaled axis")

	data = parse_data(input_path, None)

	plot_data(output_path, None)
