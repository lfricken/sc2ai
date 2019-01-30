import csv
import matplotlib.pyplot as plt
import pandas as pd
import sys
import tensorflow as tf
from typing import Iterator

sys.path.append("..")
from utils.FileEnumerable import FileEnumerable
from utils.TrainingData import *
from utils.Investments import *

time_delta = get_time_delta_seconds()

num_inputs = ZergInvestments.num_values()*2 + TerranInvestments.num_values()  # prev built units, then unit_count
num_outputs = 2  # win loss
split_input_output_count = num_outputs + ((num_inputs - num_outputs) / 2)
num_hidden_1 = int(split_input_output_count * 1)

save_directory = "brains/{}_{}_{}_sc2bot_v3_brain.ckpt".format(num_inputs, num_hidden_1, num_outputs)


def get_training_enumerable() -> Iterator[TrainingData]:
	for _ in FileEnumerable.get_analysis_enumerable():
		yield _


def get_input_type() -> tf.placeholder:
	return tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)


# Create model
def add_middle_layer(network):
	network = tf.layers.dense(inputs=network, units=num_hidden_1, activation=tf.nn.sigmoid)
	return network


def add_output_layer(network):
	network = tf.layers.dense(inputs=network, units=num_outputs, activation=tf.nn.sigmoid)
	return network


def add_softmax_layer(network):
	network = tf.nn.softmax(network)
	return network


def build_model(input_type: tf.placeholder):
	network = add_middle_layer(input_type)
	network = add_output_layer(network)
	network = add_softmax_layer(network)
	return network

def argmax(x: [int]) -> int:
	return max(range(len(x)), key=x.__getitem__)


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
		for frame, replay_data in enumerate(training_data.data):
			prediction = network.predict(
				np.concatenate([replay_data.us.previous_built_units.investments,
									 replay_data.us.unit_count.investments,
									 replay_data.them.unit_count.investments]))
			p1.append(prediction[0])
			army1.append(replay_data.us.core_values.army)
			army2.append(replay_data.them.core_values.army)
			
			# for each possible zerg unit, add to unit_count and predict
			# pick the one that has the highest win_pct and print
			unit_names=[p for p in dir(ZergInvestments) if isinstance(getattr(ZergInvestments, p), property)]
			highest_wr = 0
			chosen_units = {}
			for unit in unit_names:
				test_investment = replay_data.us.unit_count.copy()
				setattr(test_investment, unit, getattr(test_investment, unit) + 1)

				prediction = network.predict(
					np.concatenate([replay_data.us.previous_built_units.investments,
										 test_investment.investments,
										 replay_data.them.unit_count.investments]))

				chosen_units[unit] = prediction[0]

			# select 10 highest priority units
			top_10 = sorted(chosen_units.items(), key=lambda kv: kv[1], reverse=True)[:10]
			units_to_build.append(["{}s: Top ten unit(s) to build next".format(frame*5)] + top_10)

		# expand.append(replay_data.us.core_values.expand)
		# worker.append(replay_data.us.core_values.worker)
		# production.append(replay_data.us.core_values.production)

		lines_to_plot.append(PlotValues("Zerg", "red", "-", army1, 0))
		lines_to_plot.append(PlotValues("Enemy", "blue", "-", army2, 0))
		lines_to_plot.append(PlotValues("Odds Zerg Wins", "red", "-", p1, 1))
		# lines_to_plot.append(PlotValues("Production", "green", "--", production))
		# lines_to_plot.append(PlotValues("Expand", "olive", "--", expand))
		break

	with open("output.csv", "w") as f:
		 writer = csv.writer(f)
		 writer.writerows(units_to_build)

	plot_data(lines_to_plot)
	plt.show()


run_test()
