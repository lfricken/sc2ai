import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

max_x = 4


class PlotValues:
	label: str
	color: str
	style: str
	data: [int]

	def __init__(self, label, color, style, data):
		self.label = label
		self.color = color
		self.style = style
		self.data = data


def run():
	lines_to_plot: [PlotValues] = list()
	lines_to_plot.append(PlotValues("Army", "blue", "-", np.random.randn(4)))
	lines_to_plot.append(PlotValues("Expand", "red", "--", np.random.randn(4)))

	data = dict()
	data["x"] = range(0, max_x)
	for _ in lines_to_plot:
		line: PlotValues = _
		data[line.label] = line.data

	df = pd.DataFrame(data)

	for _ in lines_to_plot:
		line: PlotValues = _
		plt.plot("x", line.label, data=df, marker="", color=line.color, linewidth=2, linestyle=line.style)

	plt.ylabel("Values")
	plt.legend()
	plt.show()


run()
