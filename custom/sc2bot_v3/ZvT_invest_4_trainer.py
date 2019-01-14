# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

import random
import tensorflow as tf

from utils.TrainingValues import *

percent_train = 0.8  # what percentage of the data do we use to train rather than test?
learning_rate = 10
training_epochs = 100
num_test_samples = 30
batch_size = 30

num_inputs = TrainingValues.num_coreinvest_inputs()
num_hidden_1 = 6
num_outputs = TrainingValues.num_coreinvest_outputs()

save_directory = TrainingValues.get_save_directory(num_inputs, num_hidden_1, num_outputs)
np.set_printoptions(precision=2)


class Point:
	inputs: [int] = None
	outputs: [int] = None

	def __init__(self):
		self.inputs = []
		self.outputs = []


def randomize_data(data_array):
	np.random.shuffle(data_array)


def generate_data() -> ([[int]], [[int]], [[int]], [[int]]):
	training_data_array: [Point] = []

	for training_data in TrainingValues.get_training_enumerable():
		for i in range(len(training_data.data) - 1):
			data_point: CombinedDataPoint = training_data.data[i]
			data_point_next: CombinedDataPoint = training_data.data[i + 1]
			point = Point()
			invest_delta = np.subtract(data_point_next.us.core_values.investments, data_point.us.core_values.investments)
			point.inputs = np.concatenate((data_point.us.core_values.investments, data_point.them.core_values.investments))

			if any(i > 0 for i in invest_delta):
				invest_delta = np.divide(invest_delta, 1000.0)
				invest_delta = np.clip(invest_delta, 0, 1)
				point.outputs = invest_delta
				training_data_array.append(point)

	randomize_data(training_data_array)

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


formatter = "%.2f"


def print_manual_evaluation(session: tf.Session, network, input_type: tf.placeholder, test_input: [[int]], test_answer: [[int]]):
	# by just passing network, it implies we want the output from network
	test_output: [[[int]]] = session.run(fetches=[network], feed_dict={input_type: test_input})
	case = random.randint(0, len(test_input))
	test_output = test_output[0][case]
	test_input = test_input[case]
	test_answer = test_answer[case]

	display_input = [formatter % member for member in test_input]
	display_output = test_output.tolist()
	display_output = [formatter % member for member in display_output]
	display_answer = [formatter % member for member in test_answer]

	print("Input: {}".format(display_input))
	print("Output:{}".format(display_output))
	print("Answer:{}".format(display_answer))


def print_accuracy(session, network, input_data, output_data, input_type, output_type, before_or_after):
	cost_computation = tf.losses.mean_squared_error(predictions=network, labels=output_type)
	cost = session.run(fetches=[cost_computation], feed_dict={input_type: input_data, output_type: output_data})
	print("Error {}: {:.3f}".format(before_or_after, cost[0]))


def run():
	(train_input, train_output, test_input, test_output) = generate_data()

	class_sums = [sum(x) for x in zip(*train_output)]
	for i in range(len(class_sums)):
		class_sums[i] /= len(train_output)
	display_answer = ["{:0.2f}".format(member) for member in class_sums]
	print("Class Distribution: {}".format(display_answer))

	# tf Graph input
	input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

	# Construct model
	middle_layer = tf.layers.dense(inputs=input_type, units=num_hidden_1, activation=tf.nn.sigmoid)
	network = tf.layers.dense(inputs=middle_layer, units=num_outputs, activation=tf.nn.sigmoid)

	# Define loss and optimizer
	cost_computation = tf.losses.mean_squared_error(predictions=network, labels=output_type)
	trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost_computation)

	saver = tf.train.Saver()
	with tf.Session() as session:
		session.run(tf.global_variables_initializer())

		# try to load the brain
		try:
			saver.restore(session, save_directory)
			print("Brain loaded.")  # We loaded a network!
		except ValueError:
			print("No brain found. Creating new brain.")  # There was nothing to load.

		print("")
		print_accuracy(session, network, train_input, train_output, input_type, output_type, "on train before")
		print_accuracy(session, network, test_input, test_output, input_type, output_type, "on test before")
		print_manual_evaluation(session, network, input_type, test_input, test_output)

		print("")
		print("Training.")

		num_samples = len(train_input)
		num_batches = num_samples // batch_size

		for epoch in range(training_epochs):
			avg_cost = 0

			# batches should actually not be all the data
			batch_begin = 0
			for batch in range(num_batches):
				batch_end = batch_begin + batch_size
				t, cost = session.run(fetches=[trainer, cost_computation], feed_dict={input_type: train_input[batch_begin:batch_end], output_type: train_output[batch_begin:batch_end]})

			if epoch % 10 == 0:
				print("")
				print("Epoch {} Cost: {}".format(epoch, avg_cost))
				print_accuracy(session, network, train_input, train_output, input_type, output_type, "on training after")
				print_accuracy(session, network, test_input, test_output, input_type, output_type, "on test after")
				print_manual_evaluation(session, network, input_type, test_input, test_output)

		print("")
		print("Saving.")
		saver.save(session, save_directory)


run()
