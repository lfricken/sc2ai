from utils.TrainingValues import *
import tensorflow as tf

num_lookbacks = int(90 / get_time_delta_seconds())

num_input_investments = 0
num_inputs = ZergInvestments.num_values()
num_hidden_1 = 10
regularize = 0.0001
num_outputs = ZergInvestments.num_values()
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

	W1 = tf.get_variable("weights1", [num_inputs, num_hidden_1], regularizer=None)
	b1 = tf.get_variable("biases1", [num_hidden_1])
	network = tf.nn.sigmoid((tf.matmul(input_type, W1) + b1), name='activationLayer1')

	W2 = tf.get_variable("weights2", [num_hidden_1, num_outputs], regularizer=None)
	b2 = tf.get_variable("biases2", [num_outputs])
	network = tf.nn.sigmoid((tf.matmul(network, W2) + b2), name='activationLayer2')

	return input_type, network, output_type


def extract_data(training_data: TrainingData) -> [Point]:
	training_data_array: [Point] = []
	deltas = []
	for i in range(1):
		deltas.append(np.zeros((len(training_data.data[i].us.unit_count_deltas.investments))))

	for i in range(len(training_data.data)):
		data_point: CombinedDataPoint = training_data.data[i]
		purchases = np.clip(data_point.us.unit_count_deltas.investments, a_min=0, a_max=10000)
		if purchases.any() > 0:
			deltas.append(purchases)

	for i in range(len(deltas) - 1):
		current: [int] = np.zeros(num_inputs)
		current[TrainingValues.argmax(deltas[i])] = 1
		# current[0] = 1

		next_: [int] = np.zeros(num_inputs)
		next_[TrainingValues.argmax(deltas[i + 1])] = 1
		# next_[0] = 1

		point = Point()
		# lookbacks = deltas[-num_lookbacks:]
		# lookbacks = np.array(lookbacks).flatten()

		# point.inputs = np.concatenate((data_point.us.core_values.investments, data_point.them.core_values.investments))
		point.inputs = current
		point.outputs = next_

		training_data_array.append(point)

	return training_data_array


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
