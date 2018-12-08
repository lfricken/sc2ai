# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

import sys
# TODO: package and install this repo so we don't have to deal with relative imports
sys.path.append("..")

import random
import tensorflow as tf
from typing import Iterator

from utils.FileEnumerable import FileEnumerable
from utils.TrainingData import *

num_inputs = ZergInvestments.num_values()*2 + TerranInvestments.num_values()  # prev built units, then unit_count
num_outputs = 2  # win loss
split_input_output_count = num_outputs + ((num_inputs - num_outputs) / 2)
num_hidden_1 = int(split_input_output_count * 1)

save_directory = "brains/{}_{}_{}_sc2bot_v3_brain.ckpt".format(num_inputs, num_hidden_1, num_outputs)

percent_train = 0.5  # what percentage of the data do we use to train rather than test?
learning_rate = 10
training_epochs = 100
num_test_samples = 30
batch_size = 30
np.set_printoptions(precision=2)


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

class Point:
	inputs: [int] = None
	outputs: [int] = None

	def __init__(self):
		self.inputs = []
		self.outputs = []

def argmax(x: [int]) -> int:
	return max(range(len(x)), key=x.__getitem__)


def randomize_data(data_array):
	np.random.shuffle(data_array)


def generate_data() -> ([[int]], [[int]], [[int]], [[int]]):
	training_data_array: [Point] = []

	for training_data in get_training_enumerable():
		for data_point in training_data.data:
			point = Point()
			point.inputs = np.concatenate([data_point.us.previous_built_units.investments,
													 # data_point.them.previous_built_units.investments,  # TODO: is this needed? probably not, if from p1's perspective
													 data_point.us.unit_count.investments,
													 data_point.them.unit_count.investments])
			point.outputs = data_point.who_won
			training_data_array.append(point)

	randomize_data(training_data_array)

	train_input: [[int]] = []
	train_output: [[int]] = []
	test_input: [[int]] = []
	test_output: [[int]] = []

	num_train = len(training_data_array) * percent_train
	count = 0
	for point in training_data_array:
		count += 1
		if count < num_train:
			train_input.append(point.inputs)
			train_output.append(point.outputs)
		else:
			test_input.append(point.inputs)
			test_output.append(point.outputs)

	return train_input, train_output, test_input, test_output


format = "%.2f"


def print_manual_evaluation(session: tf.Session, network, input_type: tf.placeholder, test_input: [[int]],
                            test_answer: [[int]]):
	# by just passing network, it implies we want the output from network
	test_output: [[[int]]] = session.run(fetches=[network], feed_dict={input_type: test_input})
	case = random.randint(0, len(test_input))
	test_output = test_output[0][case]
	test_input = test_input[case]
	test_answer = test_answer[case]

	display_input = [format % member for member in test_input]
	display_output = test_output.tolist()
	output = argmax(display_output)
	answer = argmax(test_answer)
	display_output = [format % member for member in display_output]
	display_answer = [format % member for member in test_answer]

	print("Input:  {}".format(display_input))
	print("Output:{} {}".format(output, display_output))
	print("Answer:{} {}".format(answer, display_answer))


def print_accuracy(session, network, input_data, output_data, input_type, output_type, before_or_after):
	# Test model
	# TODO: we need to test with data the network hasn't seen to make sure it's not over-fitting
	tests = []
	compute_correct_prediction = tf.equal(tf.argmax(network, 1), tf.argmax(output_type, 1))
	accuracy: tf.reduce_mean = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
	accuracy_value = session.run(fetches=[accuracy], feed_dict={input_type: input_data, output_type: output_data})
	tests.append(accuracy_value)
	print("Accuracy {}: {:.2f}%".format(before_or_after, np.mean(tests) * 100))


def run():
	(train_input, train_output, test_input, test_output) = generate_data()

	class_sums = [sum(x) for x in zip(*train_output)]
	for i in range(len(class_sums)):
		class_sums[i] /= len(train_output)
	display_answer = ["{:0.2f}".format(member) for member in class_sums]
	print("Class Distribution: {}".format(display_answer))

	# tf Graph input
	input_type = get_input_type()
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

	# Construct model
	network = build_model(input_type)

	# Define loss and optimizer
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=network, labels=output_type))
	trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost)

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
				# fetches determines what to "compute"

				# passing trainer implies you want to compute, and therefor influence, the values of the network
				t, c = session.run(fetches=[trainer, cost],
				                   feed_dict={input_type: train_input[batch_begin:batch_end],
				                              output_type: train_output[batch_begin:batch_end]})
				avg_cost += c / num_batches
				batch_begin += batch_size

			if epoch % 10 == 0:
				print("")
				print("Epoch {} Cost: {}".format(epoch, avg_cost))
				print_accuracy(session, network, train_input, train_output, input_type, output_type,
				               "on training after")
				print_accuracy(session, network, test_input, test_output, input_type, output_type, "on test after")
				print_manual_evaluation(session, network, input_type, test_input, test_output)

		print("")
		print("Saving.")
		saver.save(session, save_directory)


run()
