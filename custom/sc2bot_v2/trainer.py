# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

from typing import Iterator

import numpy as np
import tensorflow as tf

from utils.FileEnumerable import FileEnumerable
from utils.Investments import Investments
from utils.TrainingData import DataPoint
from utils.TrainingData import TrainingData

# Parameters
learning_rate = 10
training_epochs = 10
num_test_samples = 30

num_inputs = Investments.num_investment_options() * 2
num_hidden_1 = 30
num_outputs = 2  # win loss

save_directory = "brains/{}_{}_{}_sc2bot_v2_brain.ckpt".format(num_inputs, num_hidden_1, num_outputs)


# Create model
def add_middle_layer(existing_network):
	out = tf.layers.dense(inputs=existing_network, units=num_hidden_1, activation=tf.nn.sigmoid)
	return out


def add_output_layer(existing_network):
	out = tf.layers.dense(inputs=existing_network, units=num_outputs, activation=tf.nn.sigmoid)
	return out


def add_softmax_layer(existing_network) -> tf.nn.softmax:
	out = tf.nn.softmax(existing_network)
	return out


def get_training_enumerable() -> Iterator[TrainingData]:
	for _ in FileEnumerable.get_analysis_enumerable():
		yield _


def randomize_data(data_array: [DataPoint]):
	for i in range(len(data_array)):
		if np.random.randint(0, 2) == 1:  # flip which player slot won
			data_array[i].inputs = np.roll(data_array[i].inputs, int(num_inputs / 2))
			data_array[i].outputs = np.roll(data_array[i].outputs, int(num_outputs / 2))
		else:
			data_array[i].outputs = np.array(data_array[i].outputs)

	np.random.shuffle(data_array)


def generate_data() -> ([[int]], [[int]]):
	training_data_array: [DataPoint] = []
	for _ in FileEnumerable.get_analysis_enumerable():
		data: TrainingData = _
		training_data_array = np.append(training_data_array, data.data_points)

	randomize_data(training_data_array)

	_input_array: [[int]] = []
	_output_array: [[int]] = []
	for _ in training_data_array:
		data: DataPoint = _
		_input_array.append(data.inputs)
		_output_array.append(data.outputs)

	return _input_array, _output_array


def print_manual_evaluation(network: tf.nn.softmax, input_type: tf.placeholder):
	test_input = [[0, 0, 400, 400, 400, 400, 400, 400]]
	# by just passing network, it implies we want the output from network
	test_output = network.eval({input_type: test_input})
	print("Odds players winning given {}: {} ".format(test_input, test_output))


def print_accuracy(network, input_data, output_data, input_type, output_type, before_or_after: str):
	# Test model
	# TODO: we need to test with data the network hasn't seen to make sure it's not over-fitting
	tests = []
	compute_correct_prediction = tf.equal(tf.round(network), tf.round(output_type))
	accuracy: tf.reduce_mean = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
	tests.append(accuracy.eval({input_type: input_data, output_type: output_data}))
	print("Accuracy {}: {:.2f}%".format(before_or_after, np.mean(tests) * 100))


def run():
	(input_data_full, output_data_full) = generate_data()

	# tf Graph input
	input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

	# Construct model
	network = add_middle_layer(input_type)
	network = add_softmax_layer(add_output_layer(network))
	# Define loss and optimizer
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=network, labels=output_type))
	trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost)

	saver = tf.train.Saver()
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

		# try to load the brain
		try:
			saver.restore(sess, save_directory)
			print("Brain loaded.")  # We loaded a network!
		except ValueError:
			print("No brain found. Creating new brain.")  # There was nothing to load.

		print_accuracy(network, input_data_full, output_data_full, input_type, output_type, "before")
		print_manual_evaluation(network, input_type)

		print("Training.")
		for epoch in range(training_epochs):
			total_batches = 30

			# batches should actually not be all the data
			for batch in range(total_batches):
				# fetches determines what to "compute"
				# passing trainer implies you want to compute, and therefor influence, the values of the network
				sess.run(fetches=[trainer], feed_dict={input_type: input_data_full, output_type: output_data_full})

		print("Saving.")
		saver.save(sess, save_directory)

		print_accuracy(network, input_data_full, output_data_full, input_type, output_type, "after")
		print_manual_evaluation(network, input_type)


run()
