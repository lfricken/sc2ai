import matplotlib.pyplot as plt
import pandas as pd

from utils.NetworkValues import *
from utils.TrainingData import *

time_delta = get_time_delta_seconds()


class Network:
	session: tf.Session
	input_type: tf.placeholder
	network = None
	save_directory: str

	def __init__(self):
		self.save_directory = save_directory
		self.session = tf.Session()
		self.input_type = get_input_type()
		self.network = build_model(self.input_type)
		saver = tf.train.Saver()
		saver.restore(self.session, self.save_directory)

	def predict(self, input_data: [int]) -> [int]:
		output: [[[int]]] = self.session.run(fetches=[self.network], feed_dict={self.input_type: [input_data]})
		return output[0][0]


class PlotValues:
	label: str
	color: str
	style: str
	data: [int]
	plot: int

	def __init__(self, label, color, style, data, plot):
		self.label = label
		self.color = color
		self.style = style
		self.data = data
		self.plot = plot


def plot_data(lines: [PlotValues], plot: int):
	data = dict()
	data["x"] = np.arange(0, time_delta * len(lines[0].data), time_delta)
	for _ in lines:
		line: PlotValues = _
		data[line.label] = line.data

	df = pd.DataFrame(data)
	fig, ax = plt.subplots(nrows=2, ncols=1)
	for _ in lines:
		line: PlotValues = _
		col = ax[line.plot]
		col.plot("x", line.label, data=df, marker="", color=line.color, linewidth=2, linestyle=line.style)
		col.legend()
		col.set_ylabel("Value")
		col.set_xlabel("Seconds")


def run_test():
	network = Network()
	lines_to_plot1: [PlotValues] = list()
	lines_to_plot2: [PlotValues] = list()
	for _ in FileEnumerable.get_analysis_enumerable():
		training_data: TrainingData = _
		p1: [int] = []
		army1: [int] = []
		army2: [int] = []
		expand: [int] = []
		worker: [int] = []
		production: [int] = []
		for __ in training_data.data:
			replay_data: CombinedDataPoint = __
			prediction = network.predict(
				np.concatenate([replay_data.us.unit_count.investments, replay_data.them.unit_count.investments]))
			p1.append(prediction[0])
			army1.append(replay_data.us.core_values.army)
			army2.append(replay_data.them.core_values.army)
		# expand.append(replay_data.us.core_values.expand)
		# worker.append(replay_data.us.core_values.worker)
		# production.append(replay_data.us.core_values.production)

		lines_to_plot1.append(PlotValues("Army1", "red", "-", army1, 0))
		lines_to_plot1.append(PlotValues("Army2", "blue", "-", army2, 0))
		lines_to_plot2.append(PlotValues("Odds", "red", "-", p1, 1))
		# lines_to_plot.append(PlotValues("Production", "green", "--", production))
		# lines_to_plot.append(PlotValues("Expand", "olive", "--", expand))

		break

	plot_data(lines_to_plot1 + lines_to_plot2, 0)

	plt.show()


run_test()
