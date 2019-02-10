from sc2ai.utils.TrainingValues import *
import tensorflow as tf

num_inputs = ZergInvestments.num_values()*2 + TerranInvestments.num_values()  # prev built units, then unit_count
num_outputs = 2  # win loss
split_input_output_count = num_outputs + ((num_inputs - num_outputs) / 2)
num_hidden_1 = int(split_input_output_count * 1)
percent_train = 0.5  # what percentage of the data do we use to train rather than test?
num_test_samples = 30
save_directory = TrainingValues.get_save_directory(num_inputs, num_hidden_1, num_outputs)


def get_input_type() -> tf.placeholder:
    return tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)


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