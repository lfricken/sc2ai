import csv
import matplotlib.pyplot as plt
import pandas as pd

from edefend_ZvT_vars2 import *

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


def plot_data(lines: [PlotValues]):
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


def run_test(target_index=0):
	network = Network()
	lines_to_plot: [PlotValues] = list()
	for index, training_data in enumerate(FileEnumerable.get_analysis_enumerable()):
		if index != target_index:
			continue

		p1: [int] = []
		army1: [int] = []
		army2: [int] = []
		expand: [int] = []
		worker: [int] = []
		production: [int] = []
		units_to_build: [str] = []
		for i in range(len(training_data.data) - 1):
			replay_data = training_data.data[i]
			prediction = network.predict(
				np.concatenate([replay_data.us.previous_built_units.investments,
									 replay_data.us.unit_count.investments,
									 replay_data.them.unit_count.investments]))
			army1.append(replay_data.us.core_values.army)
			army2.append(replay_data.them.core_values.army)

			data_point_next: CombinedDataPoint = training_data.data[i + 1]
			invest_delta = ZergInvestments()
			invest_delta.investments = np.subtract(data_point_next.us.unit_count.investments, replay_data.us.unit_count.investments)

			units_built = []
			unit_names=[p for p in dir(ZergInvestments) if isinstance(getattr(ZergInvestments, p), property)]
			for unit in unit_names:
				if isinstance(getattr(ZergInvestments, unit), property) and getattr(invest_delta, unit) > 0:
					units_built.append(unit)

			chosen_unit_delta = ZergInvestments()
			chosen_unit_delta.investments = prediction
			chosen_units = {}
			unit_names=[p for p in dir(ZergInvestments) if isinstance(getattr(ZergInvestments, p), property)]
			for unit in unit_names:
				if isinstance(getattr(ZergInvestments, unit), property) and getattr(chosen_unit_delta, unit) > 0:
					chosen_units[unit] = getattr(chosen_unit_delta, unit)
			top_10 = sorted(chosen_units.items(), key=lambda kv: kv[1], reverse=True)[:10]

			units_to_build.append(["{}s: Chosen Unit(s): ".format(i*5)] + top_10)
			units_to_build.append(["{}s: Actual Unit(s): ".format(i*5)] + units_built)


		lines_to_plot.append(PlotValues("Zerg", "red", "-", army1, 0))
		lines_to_plot.append(PlotValues("Enemy", "blue", "-", army2, 0))
		break

	with open("output.csv", "w") as f:
		 writer = csv.writer(f)
		 writer.writerows(units_to_build)

	plot_data(lines_to_plot)
	plt.show()


run_test(target_index=0)
