from utils.TrainingValues import *
import tensorflow as tf

num_inputs = TrainingValues.num_coreinvest_inputs()
num_hidden_1 = 35
num_outputs = TrainingValues.num_coreinvest_outputs()
save_directory = TrainingValues.get_save_directory(num_inputs, num_hidden_1, num_outputs)
tensorboard_dir = TrainingValues.get_tensorboard_directory()


def build_network():
	input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
	output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)
	middle_layer = tf.layers.dense(inputs=input_type, units=num_hidden_1, activation=tf.nn.sigmoid)
	network = tf.layers.dense(inputs=middle_layer, units=num_outputs, activation=tf.nn.sigmoid)

	return input_type, network, output_type
