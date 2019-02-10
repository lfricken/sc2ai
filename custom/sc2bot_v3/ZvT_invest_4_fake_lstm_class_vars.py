import tensorflow as tf

from sc2ai.utils.TrainingValues import *

num_lookbacks = int(90 / get_time_delta_seconds())

num_input_investments = 2
num_inputs = TrainingValues.num_coreinvest_outputs() * (num_input_investments + num_lookbacks)
num_hidden_1 = 6
num_outputs = TrainingValues.num_coreinvest_outputs()
save_directory = TrainingValues.get_save_directory(num_inputs, num_hidden_1, num_outputs)
tensorboard_dir = TrainingValues.get_tensorboard_directory()
percent_train = 0.8  # what percentage of the data do we use to train rather than test?


class Point:
    inputs: [int] = None
    outputs: [int] = None

    def __init__(self):
        self.inputs = []
        self.outputs = []


def build_network(is_training: bool):
    input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
    output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)
    network = tf.layers.batch_normalization(inputs=input_type, training=is_training)
    network = tf.layers.dense(inputs=network, units=num_hidden_1, activation=tf.nn.sigmoid)
    network = tf.layers.batch_normalization(inputs=network, training=is_training)
    network = tf.layers.dense(inputs=network, units=num_outputs, activation=tf.nn.sigmoid)

    return input_type, network, output_type


def extract_data(training_data: TrainingData, training_data_array: [Point]):
    deltas = []
    for i in range(num_lookbacks):
        deltas.append([0, 0, 0, 0])

    for i in range(len(training_data.data) - 1):
        data_point: CombinedDataPoint = training_data.data[i]
        data_point_next: CombinedDataPoint = training_data.data[i + 1]

        invest_delta = np.subtract(data_point_next.us.core_values.investments, data_point.us.core_values.investments)
        for _ in range(len(invest_delta)):
            if invest_delta[_] > 0:
                invest_delta[_] = 1
            else:
                invest_delta[_] = 0

        # try ignore production and expand values
        # invest_delta[1] = 0
        # invest_delta[3] = 0
        #    point.inputs[1] = 0
        #    point.inputs[3] = 0
        #    point.inputs[5] = 0
        #    point.inputs[7] = 0

        point = Point()
        lookbacks = deltas[-num_lookbacks:]
        lookbacks = np.array(lookbacks).flatten()
        # point.inputs = np.concatenate((data_point.us.core_values.investments, data_point.them.core_values.investments, lookbacks))
        point.inputs = np.concatenate((lookbacks))
        point.outputs = invest_delta

        training_data_array.append(point)
        deltas.append(invest_delta)


def format_data(training_data_array: [Point]):
    train_input: [[int]] = []
    train_output: [[int]] = []
    test_input: [[int]] = []
    test_output: [[int]] = []

    num_train = len(training_data_array) * percent_train
    count = 0
    for _ in training_data_array:
        data: Point = _
        count += 1
        if count < num_train:
            train_input.append(data.inputs)
            train_output.append(data.outputs)
        else:
            test_input.append(data.inputs)
            test_output.append(data.outputs)

    return train_input, train_output, test_input, test_output
