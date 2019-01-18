from utils.TrainingValues import *
import tensorflow as tf

num_lookbacks = int(90 / get_time_delta_seconds())

num_input_investments = 2
num_inputs = TrainingValues.num_coreinvest_outputs() * (num_input_investments + num_lookbacks)
num_hidden_1 = 16
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

	W1 = tf.Variable(tf.truncated_normal([num_inputs, num_hidden_1]), name='weights1')
	b1 = tf.Variable(tf.truncated_normal([num_hidden_1]), name='biases1')
	network = tf.nn.tanh((tf.matmul(input_type, W1) + b1), name='activationLayer1')

	W2 = tf.Variable(tf.random_normal([num_hidden_1, num_outputs]), name='weights2')
	b2 = tf.Variable(tf.random_normal([num_outputs]), name='biases2')
	network = tf.nn.tanh((tf.matmul(network, W2) + b2), name='activationLayer2')

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

		deltas[-1] = np.add(invest_delta, deltas[-1])
		deltas[-2] = np.add(invest_delta, deltas[-2])
		deltas[-3] = np.add(invest_delta, deltas[-3])
		deltas.append(invest_delta)
		current_delta = deltas[-3]

		point = Point()
		lookbacks = deltas[-(num_lookbacks + 3):-3]
		lookbacks = np.array(lookbacks).flatten()

		# point.inputs = np.concatenate((data_point.us.core_values.investments, data_point.them.core_values.investments, lookbacks))
		point.inputs = np.concatenate(([0, 0, 0, 0, 0, 0, 0, 0], lookbacks))
		point.outputs = current_delta

		training_data_array.append(point)


def format_data(training_data_array: [Point]):
	train_input: [[int]] = []
	train_output: [[int]] = []
	test_input: [[int]] = []
	test_output: [[int]] = []

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
