from tensorflow.python.keras import activations

from utils.TrainingValues import *
import tensorflow as tf

num_lookbacks = int(0 / get_time_delta_seconds())

num_inputs = ZergInvestments.num_values() + TerranInvestments.num_values()
num_hidden_1 = 8
regularize = 0.001
num_outputs = 1
percent_train = 0.8  # what percentage of the data do we use to train rather than test?

save_directory = TrainingValues.get_save_directory(num_inputs, num_hidden_1, num_outputs)
tensorboard_dir = TrainingValues.get_tensorboard_directory()
formatter = "%.4f"


class Point:
	inputs: [int] = None
	outputs: [int] = None

	def __init__(self):
		self.inputs = []
		self.outputs = []


def print_manual_evaluation(session: tf.Session, network, input_type: tf.placeholder, test_input: [[int]]):
	test_output: [[[int]]] = session.run(fetches=[network], feed_dict={input_type: test_input})

	display_input = [formatter % member for member in test_input[0]]
	display_output = [formatter % member for member in test_output[0][0]]

	print("Input: {}".format(display_input))
	print("Output:{}".format(display_output))


def build_network(is_training: bool):
	input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

	reg = tf.contrib.layers.l2_regularizer(scale=regularize)

	network = tf.layers.dense(inputs=input_type, units=num_hidden_1, activation=tf.nn.tanh, kernel_regularizer=reg)
	network = tf.layers.dense(inputs=network, units=num_outputs, activation=tf.nn.tanh, kernel_regularizer=reg)

	return input_type, network, output_type


def extract_data(training_data: TrainingData, training_data_array: [Point]):
	for i in range(len(training_data.data)):
		data_point: CombinedDataPoint = training_data.data[i]

		point = Point()
		point.inputs = np.concatenate((data_point.us.unit_count.investments, data_point.them.unit_count.investments))
		point.outputs = np.array([data_point.who_won[0]]).astype(int)

		# point.inputs = np.roll(point.inputs, len(point.inputs))
		# point.outputs = np.roll(point.outputs, len(point.outputs))

		training_data_array.append(point)


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
