from tensorflow.python.keras import activations

from sc2ai.utils.TrainingValues import *
import tensorflow as tf

num_lookbacks = int(0 / get_time_delta_seconds())

num_input_investments = 2
num_inputs = TrainingValues.num_coreinvest_outputs() * (num_input_investments + num_lookbacks)
num_hidden_1 = 6
regularize = 0.0
num_outputs = TrainingValues.num_coreinvest_outputs()
save_directory = TrainingValues.get_save_directory(num_inputs, num_hidden_1, num_outputs)
tensorboard_dir = TrainingValues.get_tensorboard_directory()
percent_train = 0.8  # what percentage of the data do we use to train rather than test?


class Point:
	inputs: [int] = None
	outputs: [int] = None

	def __init__(self):
		self.inputs = []
		self.outputs = []


def build_network(is_training: bool):
	input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

	reg = tf.contrib.layers.l2_regularizer(scale=regularize)

	network = tf.layers.dense(inputs=input_type, units=num_hidden_1, activation=tf.nn.sigmoid)
	network = tf.layers.dense(inputs=network, units=num_hidden_1, activation=tf.nn.sigmoid)
	network = tf.layers.dense(inputs=network, units=num_outputs, activation=tf.nn.tanh)

	return input_type, network, output_type


def extract_data(training_data: TrainingData, training_data_array: [Point]):
	deltas = []
	for i in range(num_lookbacks + 3):
		deltas.append([0, 0, 0, 0])

	for i in range(len(training_data.data) - 1):
		data_point: CombinedDataPoint = training_data.data[i]
		data_point_next: CombinedDataPoint = training_data.data[i + 1]

		invest_delta = np.subtract(data_point_next.us.core_values.investments, data_point.us.core_values.investments)
		invest_delta = np.divide(invest_delta, 1000.0)
		invest_delta = np.clip(invest_delta, 0, 1)

		# try ignore production and expand values
		# invest_delta[1] = 0
		# invest_delta[3] = 0
		#	point.inputs[1] = 0
		#	point.inputs[3] = 0
		#	point.inputs[5] = 0
		#	point.inputs[7] = 0

		point = Point()
		lookbacks = deltas[-num_lookbacks:]
		lookbacks = np.array(lookbacks).flatten()

		point.inputs = np.concatenate((data_point.us.core_values.investments, data_point.them.core_values.investments))
		point.outputs = invest_delta

		training_data_array.append(point)
		deltas.append(invest_delta)


class Normalizer:
	offsets: [float]
	scalars: [float]

	def __init__(self, data: [[float]], center, norm_range):
		maxs: np.ndarray = np.array(data).max(axis=0)
		mins: np.ndarray = np.array(data).min(axis=0)

		ranges = np.subtract(maxs, mins)
		averages = np.add(maxs, mins)
		averages = np.multiply(averages, 0.5)
		self.offsets = np.negative(averages)  # we are taking the average between max and min

		make_center = np.full((len(self.offsets)), center)
		self.offsets = np.add(self.offsets, make_center)

		self.scalars = np.multiply(ranges, 1.0 / norm_range)
		self.scalars = np.reciprocal(self.scalars)

		return

	def normalize_data(self, data: [[float]]) -> [[float]]:
		data = np.add(data, self.offsets)
		data = np.multiply(data, self.scalars)
		return data

	def unnormalize_data(self, data: [[float]]) -> [[float]]:
		data = np.divide(data, self.scalars)
		data = np.subtract(data, self.offsets)
		return data


def format_data(training_data_array: [Point]):
	train_input: [[float]] = []
	train_output: [[float]] = []
	test_input: [[float]] = []
	test_output: [[float]] = []

	num_train = len(training_data_array) * percent_train
	count = 0
	for _ in training_data_array:
		data: Point = _
		count += 1
		if count < num_train:
			train_input.append(data.inputs)
			train_output.append(data.outputs)
		else:
			test_input.append(data.inputs)
			test_output.append(data.outputs)

	return train_input, train_output, test_input, test_output


def unit_tests():
	print("Running unit test.")
	fake_data = [[10, 10, 10, 10, 3], [9, 8, 7, 6, 1], [-10, 0, 6, 0, -1]]
	norm1 = Normalizer(fake_data, 0, 2)

	fake_data = norm1.normalize_data(fake_data)
	print(fake_data)


if __name__ == "__main__":
	unit_tests()
