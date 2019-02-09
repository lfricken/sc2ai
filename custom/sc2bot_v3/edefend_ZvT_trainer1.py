# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

import random
import sys
import tensorflow as tf
from typing import Iterator

from edefend_ZvT_vars1 import *
from sc2ai.utils.FileEnumerable import FileEnumerable
from sc2ai.utils.TrainingData import *

learning_rate = 10
training_epochs = 100
batch_size = 30
np.set_printoptions(precision=2)


def randomize_data(data_array):
	np.random.shuffle(data_array)


def generate_data() -> ([[int]], [[int]], [[int]], [[int]]):
	training_data_array: [Point] = []

	for training_data in TrainingValues.get_training_enumerable():
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
	output = TrainingValues.argmax(display_output)
	answer = TrainingValues.argmax(test_answer)
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
