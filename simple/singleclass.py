# inputs N dimensional (0,1)
# outputs M dimensional (0,1) where a single output value should be 1, and the rest should be 0

from __future__ import print_function

import numpy as np
import tensorflow as tf

learning_rate = 10
total_training_sessions = 500

num_inputs = 1
num_hidden_1 = 2
num_outputs = 2


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
	# for a single class, we should check accuracy by comparing the index of the greatest value
	accuracy = tf.equal(tf.argmax(network), tf.argmax(output_type))
	accuracy = tf.reduce_mean(tf.cast(accuracy, "float"))
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
	# softmax should be used when the output values should sum to 1
	cost_computation = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=network, labels=output_type))
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
