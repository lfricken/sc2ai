# same as singleclass but it tries to load and save the network

from __future__ import print_function

import numpy as np
import tensorflow as tf

learning_rate = 10
total_training_sessions = 500

num_inputs = 1
num_hidden_1 = 2
num_outputs = 2
save_directory = "brains/{}_{}_{}_brain.ckpt".format(num_inputs, num_hidden_1, num_outputs)


# Data
def generate_data() -> ([[int]], [[int]]):
	_input_array = [[1], [0]]
	_output_array = [[1, 0], [0, 1]]

	return _input_array, _output_array


# Test Output
def print_manual_evaluation(session: tf.Session, network, input_type: tf.placeholder):
	test_input = [[1]]
	test_output = session.run(fetches=[network], feed_dict={input_type: test_input})
	print("Output given {}: {} ".format(test_input, np.around(test_output, decimals=2)))


# Test Error
def print_accuracy(session, network, input_data, output_data, input_type, output_type, before_or_after):
	compute_correct_prediction = tf.equal(tf.argmax(network, axis=1), tf.argmax(output_type, axis=1))
	accuracy = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
	calculated_accuracy = session.run(fetches=[accuracy], feed_dict={input_type: input_data, output_type: output_data})
	print("Accuracy {}: {:.2f}%".format(before_or_after, calculated_accuracy[0] * 100))


def run():
	(input_data_full, output_data_full) = generate_data()

	# tf Graph input
	input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

	# Construct model
	middle_layer = tf.layers.dense(inputs=input_type, units=num_hidden_1, activation=tf.nn.sigmoid)
	network = tf.layers.dense(inputs=middle_layer, units=num_outputs, activation=tf.nn.sigmoid)

	# Define cost and optimizer
	cost_computation = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=network, labels=output_type))
	trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost_computation)

	# Train the model
	# TODO Start Special Code
	saver = tf.train.Saver()
	# TODO End Special Code
	with tf.Session() as session:
		session.run(tf.global_variables_initializer())  # randomly initialize network

		# TODO Start Special Code
		try:
			saver.restore(session, save_directory)
			print("Brain loaded.")  # We loaded a network!
		except ValueError:
			print("No brain found. Creating new brain.")  # There was nothing to load.
		# TODO End Special Code

		print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "before")
		print_manual_evaluation(session, network, input_type)

		print("Training.")
		for _ in range(total_training_sessions):  # _ just means ignore this value
			# fetches determines what to "compute"
			# passing trainer implies you want to compute, and therefor influence, the values of the network
			cost, _ = session.run(fetches=[cost_computation, trainer], feed_dict={input_type: input_data_full, output_type: output_data_full})

		print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "after")
		print_manual_evaluation(session, network, input_type)

		# TODO Start Special Code
		print("Saving.")
		saver.save(session, save_directory)
		# TODO End Special Code


run()
