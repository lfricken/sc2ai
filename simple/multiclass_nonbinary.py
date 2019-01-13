# done
from __future__ import print_function

import numpy as np
import tensorflow as tf

learning_rate = 50
total_training_sessions = 500

num_inputs = 1
num_hidden_1 = 2
num_outputs = 2


# Data
def generate_data() -> ([[int]], [[int]]):
	_input_array = [[1], [0]]
	_output_array = [[0.75, 0], [1, 0.5]]

	return _input_array, _output_array


# Test Output
def print_manual_evaluation(session: tf.Session, network, input_type: tf.placeholder):
	test_input = [[1], [0]]
	test_output = session.run(fetches=[network], feed_dict={input_type: test_input})
	print("Output given {}: {} ".format(test_input, np.around(test_output, decimals=2)))


# Test Error
def print_accuracy(session, network, input_data, output_data, input_type, output_type, before_or_after):
	compute_error = tf.losses.mean_squared_error(predictions=network, labels=output_type)
	error = session.run(fetches=[compute_error], feed_dict={input_type: input_data, output_type: output_data})
	print("Error {}: {:.2f}".format(before_or_after, error[0]))


def run():
	(input_data_full, output_data_full) = generate_data()

	# tf Graph input
	input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

	# Construct model
	middle_layer = tf.layers.dense(inputs=input_type, units=num_hidden_1, activation=tf.nn.sigmoid)
	network = tf.layers.dense(inputs=middle_layer, units=num_hidden_1, activation=tf.nn.sigmoid)

	# Define cost and optimizer
	cost_computation = tf.reduce_mean(tf.losses.mean_squared_error(predictions=network, labels=output_type))
	trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost_computation)

	# Train the model
	with tf.Session() as session:
		session.run(tf.global_variables_initializer())  # randomly initialize network

		print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "before")
		print_manual_evaluation(session, network, input_type)

		print("Training.")
		for _ in range(total_training_sessions):  # _ just means ignore this value
			# fetches determines what to "compute"
			# passing trainer implies you want to compute, and therefor influence, the values of the network
			cost, _ = session.run(fetches=[cost_computation, trainer], feed_dict={input_type: input_data_full, output_type: output_data_full})

		print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "after")
		print_manual_evaluation(session, network, input_type)


run()
