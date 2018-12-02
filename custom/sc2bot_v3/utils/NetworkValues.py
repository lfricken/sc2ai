from typing import Iterator

import tensorflow as tf

from utils.FileEnumerable import FileEnumerable
from utils.TrainingData import *

num_inputs = ZergInvestments.num_values() + TerranInvestments.num_values()
num_outputs = 2  # win loss
split_input_output_count = num_outputs + ((num_inputs - num_outputs) / 2)
num_hidden_1 = int(split_input_output_count * 1.5)

save_directory = "brains/{}_{}_{}_sc2bot_v3_brain.ckpt".format(num_inputs, num_hidden_1, num_outputs)


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


def argmax(x: [int]) -> int:
	return max(range(len(x)), key=x.__getitem__)
