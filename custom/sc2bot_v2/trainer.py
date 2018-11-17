# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

import numpy as np
import tensorflow as tf

from utils.FileEnumerable import FileEnumerable
from utils.Investments import Investments
from utils.TrainingData import TrainingData

# Parameters
learning_rate = 0.2
training_epochs = 15
batch_size = 100

num_labels = 1  # win loss odds
num_inputs = Investments.num_investment_options() * 2


# Create model
def add_middle_layer(existing_network):
	out = tf.layers.dense(inputs=existing_network, units=30, activation=tf.nn.sigmoid)
	return out


def add_output_layer(existing_network):
	out = tf.layers.dense(inputs=existing_network, units=num_labels, activation=tf.nn.sigmoid)
	return out


def add_softmax_layer(existing_network):
	out = tf.nn.softmax(existing_network)
	return out


for _ in FileEnumerable.get_analysis_enumerable():
	training_data: TrainingData = _
	# tf Graph input
	networkInput = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	networkOutput = tf.placeholder(shape=[None, num_labels], dtype=tf.float32)

	# randomly flip data
	for i in range(len(training_data.inputs)):
		if np.random.randint(0, 2) == 1:
			training_data.inputs[i] = np.roll(training_data.inputs[i], Investments.num_investment_options())
			training_data.outputs[i][0] = not training_data.outputs[i][0]  # flip who won

	# Construct model
	network = add_middle_layer(networkInput)
	network = add_output_layer(network)

	# Define loss and optimizer
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=network, labels=networkOutput))
	trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost)

	saver = tf.train.Saver()
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
		writer = tf.summary.FileWriter("output", sess.graph)

		if (False):
			saver.restore(sess, "brains/")
		else:
			for epoch in range(training_epochs):
				total_batches = 5

				avg_cost = 0.
				j = 0
				for i in range(total_batches):
					j += 1
					correct_inputs = training_data.inputs
					correct_outputs = training_data.outputs

					summary, cost_value, output = sess.run(fetches=[trainer, cost, network],
					                      feed_dict={networkInput: correct_inputs, networkOutput: correct_outputs})

					avg_cost += cost_value / total_batches
				print("Epoch: {}".format(epoch + 1) + " Cost = {:.5f}".format(avg_cost))
			print("Done Training.")
		saver.save(sess, "brains/")

		# Test model
		correct_prediction = tf.equal(tf.argmax(network, 1), tf.argmax(networkOutput, 1))

		accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

		correct_inputs = training_data.inputs
		correct_outputs = training_data.outputs
		print("Accuracy:", accuracy.eval({networkInput: correct_inputs, networkOutput: correct_outputs}))

		writer.close()
