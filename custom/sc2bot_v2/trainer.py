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
learning_rate = 2
training_epochs = 20
num_test_samples = 30

num_inputs = Investments.num_investment_options() * 2
num_hidden_1 = 30
num_outputs = 2  # win loss

save_directory = "brains/sc2bot_v2_brain.ckpt"


# Create model
def add_middle_layer(existing_network):
	out = tf.layers.dense(inputs=existing_network, units=num_hidden_1, activation=tf.nn.sigmoid)
	return out


def add_output_layer(existing_network):
	out = tf.layers.dense(inputs=existing_network, units=num_outputs, activation=tf.nn.sigmoid)
	return out


def add_softmax_layer(existing_network):
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


(input_array, output_array) = generate_data()

# tf Graph input
networkInput = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
networkOutput = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

# Construct model
network = add_middle_layer(networkInput)
network = add_softmax_layer(add_output_layer(network))

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=network, labels=networkOutput))
trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost)

saver = tf.train.Saver()
with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	# writer = tf.summary.FileWriter("output", sess.graph)  # write the graph?

	try:
		saver.restore(sess, save_directory)
		print("Brain loaded.")  # We loaded a network!
	except ValueError:
		print("No brain found. Creating new brain.")  # There was nothing to load.

	# Test model
	# TODO: we need to test with data the network hasn't seen to make sure it's not over-fitting
	tests = []
	for sample in range(num_test_samples):
		compute_correct_prediction = tf.equal(tf.round(network), tf.round(networkOutput))
		accuracy = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
		correct_inputs = input_array
		correct_outputs = output_array
		tests.append(accuracy.eval({networkInput: correct_inputs, networkOutput: correct_outputs}))
	print("Accuracy before: {:.2f}%".format(np.mean(tests) * 100))

	print("Training.")
	for epoch in range(training_epochs):
		total_batches = 4

		for batch in range(total_batches):
			correct_inputs = input_array
			correct_outputs = output_array

			# fetches determines what to "compute"
			# passing the network implies you want to compute the values that the network produces
			# passing trainer implies you want to compute, and therefor influence, the values of the network
			# passing a computation for cost lets you return the value computed by the cost algorithm
			summary, cost_value, output = sess.run(fetches=[trainer, cost, network],
			                                       feed_dict={networkInput: correct_inputs,
			                                                  networkOutput: correct_outputs})

		tests = []
		for sample in range(num_test_samples):
			compute_correct_prediction = tf.equal(tf.round(network), tf.round(networkOutput))
			accuracy = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
			correct_inputs = input_array
			correct_outputs = output_array
			tests.append(accuracy.eval({networkInput: correct_inputs, networkOutput: correct_outputs}))
		print("Epoch {} accuracy: {:.2f}%".format(epoch + 1, np.mean(tests) * 100))

	print("Saving.")
	saver.save(sess, save_directory)

	# Test model
	# TODO: we need to test with data the network hasn't seen to make sure it's not over-fitting
	tests = []
	for sample in range(num_test_samples):
		compute_correct_prediction = tf.equal(tf.round(network), tf.round(networkOutput))
		accuracy = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
		correct_inputs = input_array
		correct_outputs = output_array
		tests.append(accuracy.eval({networkInput: correct_inputs, networkOutput: correct_outputs}))
	print("Accuracy after: {:.2f}%".format(np.mean(tests) * 100))

# writer.close()
