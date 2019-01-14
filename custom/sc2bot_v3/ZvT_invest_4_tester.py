import matplotlib.pyplot as plt
import pandas as pd

from ZvT_invest_4_vars import *

time_delta = get_time_delta_seconds()


class Network:
	session: tf.Session
	input_type: tf.placeholder
	network = None
	save_directory: str

	def __init__(self):
		self.save_directory = save_directory
		self.session = tf.Session()
		(self.input_type, self.network, _) = build_network()
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
	xlabel: str
	ylabel: str

	def __init__(self, label, color, style, data, plot, xlabel, ylabel):
		self.label = label
		self.color = color
		self.style = style
		self.data = data
		self.plot = plot


def plot_data(lines: [PlotValues]):
	data = dict()
	data["x"] = np.arange(0, time_delta * len(lines[0].data), time_delta)
	for _ in lines:
		line: PlotValues = _
		data[line.label] = line.data

	df = pd.DataFrame(data)
	fig, ax = plt.subplots(nrows=3, ncols=1)
	for _ in lines:
		line: PlotValues = _
		col = ax[line.plot]
		col.plot("x", line.label, data=df, marker="", color=line.color, linewidth=2, linestyle=line.style)
		col.legend()

		col.set_xlabel("Seconds")
		if line.plot == 0:
			col.set_ylabel("Actual Army Value")
		if line.plot == 1:
			col.set_ylabel("Predicted Investment Deltas")
		if line.plot == 2:
			col.set_ylabel("Actual Investment Deltas")


def run_test():
	network = Network()
	lines_to_plot: [PlotValues] = list()
	for _ in FileEnumerable.get_analysis_enumerable():
		training_data: TrainingData = _
		real1: [int] = []
		real2: [int] = []
		real3: [int] = []
		real4: [int] = []
		p1: [int] = []
		p2: [int] = []
		p3: [int] = []
		p4: [int] = []
		army1: [int] = []
		army2: [int] = []
		expand: [int] = []
		worker: [int] = []
		production: [int] = []
		for i in range(len(training_data.data) - 1):
			replay_data: CombinedDataPoint = training_data.data[i]
			replay_data_next: CombinedDataPoint = training_data.data[i + 1]
			invest_delta = np.subtract(replay_data_next.us.core_values.investments, replay_data.us.core_values.investments)
			input_data = np.concatenate((replay_data.us.core_values.investments, replay_data.them.core_values.investments))
			prediction = network.predict(input_data)
			invest_delta = np.clip(invest_delta, 0, 1000)
			real1.append(invest_delta[0])
			real2.append(invest_delta[1])
			real3.append(invest_delta[2])
			real4.append(invest_delta[3])
			p1.append(prediction[0] * 1000)
			p2.append(prediction[1] * 1000)
			p3.append(prediction[2] * 1000)
			p4.append(prediction[3] * 1000)
			army1.append(replay_data.us.core_values.army)
			army2.append(replay_data.them.core_values.army)
		# expand.append(replay_data.us.core_values.expand)
		# worker.append(replay_data.us.core_values.worker)
		# production.append(replay_data.us.core_values.production)

		lines_to_plot.append(PlotValues("Zerg", "red", "-", army1, 0, "", ""))
		lines_to_plot.append(PlotValues("Enemy", "blue", "-", army2, 0, "", ""))
		lines_to_plot.append(PlotValues("Invest Army", "red", "-", p1, 1, "", ""))
		lines_to_plot.append(PlotValues("Invest Production", "blue", "-", p2, 1, "", ""))
		lines_to_plot.append(PlotValues("Invest Worker", "green", "-", p3, 1, "", ""))
		lines_to_plot.append(PlotValues("Invest Expand", "yellow", "-", p4, 1, "", ""))
		lines_to_plot.append(PlotValues("Invest Army2", "red", "-", real1, 2, "", ""))
		lines_to_plot.append(PlotValues("Invest Production2", "blue", "-", real2, 2, "", ""))
		lines_to_plot.append(PlotValues("Invest Worker2", "green", "-", real3, 2, "", ""))
		lines_to_plot.append(PlotValues("Invest Expand2", "yellow", "-", real4, 2, "", ""))
		# lines_to_plot.append(PlotValues("Production", "green", "--", production))
		# lines_to_plot.append(PlotValues("Expand", "olive", "--", expand))

		break

	plot_data(lines_to_plot)
	plt.show()


run_test()
