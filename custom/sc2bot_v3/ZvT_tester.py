import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from utils.FileEnumerable import FileEnumerable
from utils.TrainingData import *


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
	for _ in FileEnumerable.get_analysis_enumerable():
		training_data: TrainingData = _
		army: [int] = []
		expand: [int] = []
		worker: [int] = []
		production: [int] = []
		for __ in training_data.data:
			replay_data: CombinedDataPoint = __
			army.append(replay_data.us.core_values.army)
			expand.append(replay_data.us.core_values.expand)
			worker.append(replay_data.us.core_values.worker)
			production.append(replay_data.us.core_values.production)

		lines_to_plot.append(PlotValues("Army", "red", "-", army))
		lines_to_plot.append(PlotValues("Worker", "blue", "--", worker))
		lines_to_plot.append(PlotValues("Production", "green", "--", production))
		lines_to_plot.append(PlotValues("Expand", "olive", "--", expand))

		break

	data = dict()
	data["x"] = np.arange(0, 5*len(lines_to_plot[0].data), 5)
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
