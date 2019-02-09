import matplotlib.pyplot as plt
import pandas as pd

from ZvT_win_vars import *
from sc2ai.utils.TrainingValues import *

test_only = False
normalize_output = False
doPrediction = True

sub_dir = ""
if test_only:
	sub_dir = "test"

time_delta = get_time_delta_seconds()


class Network:
	session: tf.Session
	input_type: tf.placeholder
	network = None
	save_directory: str

	def __init__(self):
		self.save_directory = save_directory
		self.session = tf.Session()
		(self.input_type, self.network, _) = build_network(False)
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

	def __init__(self, label, color, style, data, plot, _xlabel, _ylabel):
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

	if normalize_output:
		for i in range(1, 2):
			ax[i].set_ylim([-1, 1])
	else:
		for i in range(1, 2):
			ax[i].set_ylim([0, 1])

	for _ in lines:
		line: PlotValues = _
		col = ax[line.plot]
		col.plot("x", line.label, data=df, marker="", color=line.color, linewidth=2, linestyle=line.style)
		col.legend()

		col.set_xlabel("Minutes")
		if line.plot == 0:
			col.set_ylabel("Actual Army Value")
		if line.plot == 1:
			col.set_ylabel("Predicted Investment Deltas")
		if line.plot == 2:
			col.set_ylabel("Actual Investment Deltas")


def chooser(network: Network, delta: float, current: [int]) -> int:
	odds = []
	investment_options = []
	for i in range(len(current) // 2):
		investments = np.copy(current)
		investments[i] += delta
		result = network.predict(investments)
		odds.append(result[0])
		investment_options.append(investments)

	best_pos = TrainingValues.argmax(odds)
	return investment_options[best_pos]


def run_test():
	network = Network()
	# print_manual_evaluation(network.session, network.network, network.input_type, [[0, 0, 600, 400, 0, 0, 600, 400]])
	#
	# if doPrediction:
	# 	delta = 50.0
	# 	investment_order = [[0, 0, 600, 400, 0, 0, 600, 400]]
	#
	# 	for i in range(20):
	# 		last_invest = investment_order[-1]
	# 		next_invest = chooser(network, delta, last_invest)
	# 		investment_order.append(next_invest)

	num_replays = 6
	start = 0
	min_replay = start
	max_replay = min_replay + num_replays

	training_data_array: [Point] = []
	for _ in FileEnumerable.get_analysis_enumerable(sub_dir):
		training_data: TrainingData = _
		extract_data(training_data, training_data_array)

	input_data_full, output_data_full, _, _ = format_data(training_data_array)
	input_norm: Normalizer = Normalizer(input_data_full, 0, 2)

	count = 0
	for _ in FileEnumerable.get_analysis_enumerable(sub_dir):
		count += 1
		if count < min_replay:
			continue
		if count > max_replay:
			break

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
		# expand: [int] = []
		# worker: [int] = []
		# production: [int] = []

		training_data_array: [Point] = []
		extract_data(training_data, training_data_array)
		input_data_full, output_data_full, _, _ = format_data(training_data_array)

		input_data_full = input_norm.normalize_data(input_data_full)

		# output_norm: Normalizer = Normalizer(output_data_full, 0, 2)
		# if normalize_output:
		#	output_data_full = output_norm.normalize_data(output_data_full)

		for i in range(len(input_data_full)):
			input_data = input_data_full[i]
			output_data = output_data_full[i]

			prediction = network.predict(input_data)
			# if not normalize_output:
			#	prediction = output_norm.unnormalize_data(prediction)

			real1.append(output_data[0])
			#			real3.append(output_data[2])
			#			real4.append(output_data[3])
			p1.append(prediction[0])
			#			p3.append(prediction[2])
			#			p4.append(prediction[3])
			army1.append(input_data[0])
			army2.append(input_data[4])
		# expand.append(replay_data.us.core_values.expand)
		# worker.append(replay_data.us.core_values.worker)
		# production.append(replay_data.us.core_values.production)

		lines_to_plot: [PlotValues] = list()
		lines_to_plot.append(PlotValues("Zerg", "red", "-", army1, 0, "", ""))
		lines_to_plot.append(PlotValues("Enemy", "blue", "-", army2, 0, "", ""))
		lines_to_plot.append(PlotValues("Invest Army", "red", "-", p1, 1, "", ""))
		#lines_to_plot.append(PlotValues("Invest Production", "blue", "-", p2, 1, "", ""))
		# lines_to_plot.append(PlotValues("Invest Worker", "green", "-", p3, 1, "", ""))
		# lines_to_plot.append(PlotValues("Invest Expand", "yellow", "-", p4, 1, "", ""))
		lines_to_plot.append(PlotValues("Invest Army2", "red", "-", real1, 2, "", ""))
		#lines_to_plot.append(PlotValues("Invest Production2", "blue", "-", real2, 2, "", ""))
		# lines_to_plot.append(PlotValues("Invest Worker2", "green", "-", real3, 2, "", ""))
		# lines_to_plot.append(PlotValues("Invest Expand2", "yellow", "-", real4, 2, "", ""))
		# lines_to_plot.append(PlotValues("Production", "green", "--", production))
		# lines_to_plot.append(PlotValues("Expand", "olive", "--", expand))

		plot_data(lines_to_plot)
		plt_man = plt.get_current_fig_manager()
		plt_man.window.wm_geometry("+200+200")
		plt.show()


run_test()
