# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

from typing import Iterator

import numpy as np
import tensorflow as tf

from utils.FileEnumerable import FileEnumerable
from utils.Investments import Investments
from utils.TrainingData import TrainingData

# Parameters
learning_rate = 0.2
training_epochs = 100

num_inputs = Investments.num_investment_options() * 2
num_hidden_1 = 30
num_labels = 2  # win loss
save_directory = "brains/sc2bot_v2_brain.ckpt"


# Create model
def add_middle_layer(existing_network):
	out = tf.layers.dense(inputs=existing_network, units=num_hidden_1, activation=tf.nn.sigmoid)
	return out


def add_output_layer(existing_network):
	out = tf.layers.dense(inputs=existing_network, units=num_labels, activation=tf.nn.sigmoid)
	out = tf.nn.softmax(logits=out)
	return out


def add_softmax_layer(existing_network):
	out = tf.nn.softmax(existing_network)
	return out


def get_training_enumerable() -> Iterator[TrainingData]:
	for data in FileEnumerable.get_analysis_enumerable():
		training_data: TrainingData = data

		# randomize the data so the network just doesn't predict the winning player
		for increment in range(len(training_data.inputs)):
			if np.random.randint(0, 2) == 0:  # 50 50
				training_data.inputs[increment] = np.roll(training_data.inputs[increment], int(num_inputs / 2))
				training_data.outputs[increment] = np.roll(training_data.outputs[increment],
				                                           int(num_labels / 2))  # flip who won

		yield training_data


training_data_array: [TrainingData] = []
for data in get_training_enumerable():
	training_data_array.append(data)

# tf Graph input
networkInput = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
networkOutput = tf.placeholder(shape=[None, num_labels], dtype=tf.float32)

# Construct model
network = add_middle_layer(networkInput)
network = add_output_layer(network)

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
	compute_correct_prediction = tf.equal(tf.round(network), tf.round(networkOutput))
	accuracy = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
	correct_inputs = training_data_array[0].inputs
	correct_outputs = training_data_array[0].outputs
	accuracy = accuracy.eval({networkInput: correct_inputs, networkOutput: correct_outputs})
	print("Accuracy before: {:.2f}%".format(accuracy * 100))

	print("Training.")
	for epoch in range(training_epochs):
		total_batches = 5
		# avg_cost = 0.

		for training_data in training_data_array:

			for batch in range(total_batches):
				correct_inputs = training_data.inputs
				correct_outputs = training_data.outputs

				# fetches determines what to "compute"
				# passing the network implies you want to compute the values that the network produces
				# passing trainer implies you want to compute, and therefor influence, the values of the network
				# passing a computation for cost lets you return the value computed by the cost algorithm
				summary, cost_value, output = sess.run(fetches=[trainer, cost, network],
				                                       feed_dict={networkInput: correct_inputs,
				                                                  networkOutput: correct_outputs})

	# avg_cost += cost_value / total_batches

	# print("Epoch: {}".format(epoch + 1) + " Cost = {:.5f}".format(avg_cost))

	print("Saving.")
	saver.save(sess, save_directory)

	# Test model
	# TODO: we need to test with data the network hasn't seen to make sure it's not over-fitting
	compute_correct_prediction = tf.equal(tf.round(network), tf.round(networkOutput))
	accuracy = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
	correct_inputs = training_data_array[0].inputs
	correct_outputs = training_data_array[0].outputs
	accuracy = accuracy.eval({networkInput: correct_inputs, networkOutput: correct_outputs})
	print("Accuracy after: {:.2f}%".format(accuracy * 100))

# writer.close()
