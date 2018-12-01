# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

from typing import Iterator

import tensorflow as tf

from utils.FileEnumerable import FileEnumerable
from utils.TrainingData import *

learning_rate = 10
training_epochs = 100
num_test_samples = 30

batch_size = 30

num_inputs = ZergInvestments.num_values() + TerranInvestments.num_values()
num_outputs = ZergInvestments.num_values()  # win loss
num_hidden_1 = num_outputs + ((num_inputs - num_outputs) / 2)

save_directory = "brains/{}_{}_{}_sc2bot_v2_brain.ckpt".format(num_inputs, num_hidden_1, num_outputs)

np.set_printoptions(precision=2)


# Create model
def add_middle_layer(network):
	network = tf.layers.dense(inputs=network, units=num_hidden_1, activation=tf.nn.sigmoid)
	return network


def add_output_layer(network):
	network = tf.layers.dense(inputs=network, units=num_outputs, activation=tf.nn.sigmoid)
	return network


def add_softmax_layer(existing_network) -> tf.nn.softmax:
	out = tf.nn.softmax(existing_network)
	return out


def get_training_enumerable() -> Iterator[TrainingData]:
	for _ in FileEnumerable.get_analysis_enumerable():
		yield _


def randomize_data(data_array):
	np.random.shuffle(data_array)


class Point:
	inputs: [int] = None
	outputs: [int] = None

	def __init__(self):
		self.inputs = []
		self.outputs = []


def argmax(x: [int]) -> int:
	return max(range(len(x)), key=x.__getitem__)

def generate_data() -> ([[int]], [[int]]):
	training_data_array: [Point] = []

	for _ in FileEnumerable.get_analysis_enumerable():
		training_data: TrainingData = _

		for _ in training_data.data:
			data_point: CombinedDataPoint = _
			if np.count_nonzero(data_point.us.unit_count_deltas.investments) > 0:
				point = Point()
				delta = data_point.us.unit_count_deltas
				start_count = data_point.us.unit_count.minus(delta)
				point.inputs = np.concatenate([start_count.investments, data_point.them.unit_count.investments])
				index_max = argmax(delta.investments)
				point.outputs = np.full(len(delta.investments), 0)
				point.outputs[index_max] = 1
				training_data_array.append(point)

	randomize_data(training_data_array)

	_input_array: [[int]] = []
	_output_array: [[int]] = []
	for _ in training_data_array:
		data = _
		_input_array.append(data.inputs)
		_output_array.append(data.outputs)

	return _input_array, _output_array


format = "%02.2f"


def print_manual_evaluation(session: tf.Session, network, input_type: tf.placeholder, test_input: [int],
                            test_answer: [int]):
	# by just passing network, it implies we want the output from network
	test_output = session.run(fetches=[network], feed_dict={input_type: [test_input]})

	display_input = [format % member for member in test_input]
	display_output = test_output[0][0].tolist()
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
	(input_data_full, output_data_full) = generate_data()

	test_input = input_data_full[0]
	test_output = output_data_full[0]

	# tf Graph input
	input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

	# Construct model
	network = add_middle_layer(input_type)
	network = add_output_layer(network)
	# Define loss and optimizer
	cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=network, labels=output_type))
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

		print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "before")
		print_manual_evaluation(session, network, input_type, test_input, test_output)

		print("Training.")

		num_samples = len(input_data_full)
		num_batches = num_samples // batch_size

		for epoch in range(training_epochs):

			test_input = input_data_full[epoch]
			test_output = output_data_full[epoch]
			avg_cost = 0

			# batches should actually not be all the data
			batch_begin = 0
			for batch in range(num_batches):
				batch_end = batch_begin + batch_size
				# fetches determines what to "compute"
				# passing trainer implies you want to compute, and therefor influence, the values of the network
				t, c = session.run(fetches=[trainer, cost], feed_dict={input_type: input_data_full[batch_begin:batch_end], output_type: output_data_full[batch_begin:batch_end]})
				avg_cost += c / num_batches
				batch_begin += batch_size

			#if epoch % 10 == 0:
			print("Epoch {} Cost: {}".format(epoch, avg_cost))
			print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "after")
			print_manual_evaluation(session, network, input_type, test_input, test_output)

		print("Saving.")
		saver.save(session, save_directory)


run()
