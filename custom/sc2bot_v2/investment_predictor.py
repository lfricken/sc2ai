# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

from typing import Iterator

import numpy as np
import tensorflow as tf

from utils.FileEnumerable import FileEnumerable
from utils.Investments import Investments
from utils.TrainingData import DataPoint
from utils.TrainingData import TrainingData

learning_rate = 0.2
training_epochs = 60

num_invest_options = Investments.num_investment_options()
num_inputs = num_invest_options * 2
num_hidden_1 = 8
num_outputs = num_invest_options

save_directory = "brains/investment_predictor/"
save_directory = save_directory + "{}_{}_{}_sc2bot_v2_brain.ckpt".format(num_inputs, num_hidden_1, num_outputs)


# Create model
def add_middle_layer(existing_network):
    out = tf.layers.dense(inputs=existing_network, units=num_hidden_1, activation=tf.nn.sigmoid)
    return out


def add_output_layer(existing_network):
    out = tf.layers.dense(inputs=existing_network, units=num_outputs, activation=tf.nn.sigmoid)
    return out


def get_training_enumerable() -> Iterator[TrainingData]:
    for _ in FileEnumerable.get_analysis_enumerable():
        yield _


def randomize_data(data_array: [DataPoint]):
    np.random.shuffle(data_array)


def setup_output(target, current_invest, next_invest):
    if not np.array_equal(current_invest, next_invest):
        delta = np.subtract(next_invest, current_invest)
        delta = np.clip(delta, 0, 100)
        delta = np.true_divide(delta, 100)
        target.outputs = [0, 0.5, 0, 0]  # delta


def generate_data() -> ([[int]], [[int]]):
    training_data_array: [DataPoint] = []
    for _ in FileEnumerable.get_analysis_enumerable():
        data: TrainingData = _
        player_1_won = data.data_points[0].outputs[0]
        for point in range(len(data.data_points) - 1):
            current_invest: DataPoint = data.data_points[point]
            next_invest: DataPoint = data.data_points[point + 1]  # get next investment

            if player_1_won:
                current_invest.inputs = np.roll(current_invest.inputs, 4)
            setup_output(current_invest, current_invest.inputs[0:4], next_invest.inputs[0:4])

            if len(current_invest.outputs) == 4 and max(current_invest.outputs) > 0:
                training_data_array.append(current_invest)

    randomize_data(training_data_array)

    _input_array: [[int]] = []
    _output_array: [[int]] = []
    for _ in training_data_array:
        data: DataPoint = _
        _input_array.append(data.inputs)
        _output_array.append(data.outputs)

    return _input_array, _output_array


def print_manual_evaluation(session: tf.Session, network, input_type: tf.placeholder):
    test_input = [[400, 150, 600, 400, 0, 0, 600, 400]]
    # by just passing network, it implies we want the output from network
    test_output = session.run(fetches=[network], feed_dict={input_type: test_input})
    print("Odds players winning given {}: {} ".format(test_input, test_output))


def print_accuracy(session, network, input_data, output_data, input_type, output_type, before_or_after):
    # Test model
    # TODO: we need to test with data the network hasn't seen to make sure it's not over-fitting
    tests = []
    compute_correct_prediction = tf.equal(tf.argmax(network, 1), tf.argmax(output_type, 1))
    accuracy: tf.reduce_mean = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"))
    accuracy_value, output = session.run(fetches=[accuracy, network],
                                         feed_dict={input_type: input_data, output_type: output_data})
    tests.append(accuracy_value)
    print("Accuracy {}: {:.2f}%".format(before_or_after, np.mean(tests) * 100))


def run():
    (input_data_full, output_data_full) = generate_data()

    # tf Graph input
    input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32)
    output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32)

    # Construct model
    network = add_middle_layer(input_type)
    network = add_output_layer(network)
    # Define loss and optimizer
    cost = tf.reduce_mean(tf.losses.mean_squared_error(predictions=network, labels=output_type))
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
        print_manual_evaluation(session, network, input_type)

        print("Training.")

        batches_per_epoch = 50
        samples_per_batch = int(int(len(input_data_full)) / int(batches_per_epoch))


        for epoch in range(training_epochs):
            lower = 0
            higher = samples_per_batch
            c = 0
            # batches should actually not be all the data
            for batch in range(batches_per_epoch):
                # fetches determines what to "compute"
                # passing trainer implies you want to compute, and therefor influence, the values of the network
                _summary, c = session.run(fetches=[trainer, cost],
                                          feed_dict={input_type: input_data_full[lower:higher],
                                                     output_type: output_data_full[lower:higher]})

            lower += samples_per_batch
            higher += samples_per_batch

            print(c)

        print("Saving.")
        saver.save(session, save_directory)

        print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "after")
        print_manual_evaluation(session, network, input_type)


run()
