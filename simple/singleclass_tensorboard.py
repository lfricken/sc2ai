# same as singleclass but it uses tensorboard

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
    compute_correct_prediction = tf.equal(tf.argmax(network, axis=1), tf.argmax(output_type, axis=1))
    accuracy_compute = tf.reduce_mean(tf.cast(compute_correct_prediction, "float"), name="End_Print_Accuracy_Calculation")
    error = session.run(fetches=[accuracy_compute], feed_dict={input_type: input_data, output_type: output_data})
    print("Accuracy {}: {:.2f}%".format(before_or_after, error[0] * 100))


def run():
    (input_data_full, output_data_full) = generate_data()

    # tf Graph input
    input_type = tf.placeholder(shape=[None, num_inputs], dtype=tf.float32, name="Input_Placeholder")
    output_type = tf.placeholder(shape=[None, num_outputs], dtype=tf.float32, name="Output_Placeholder")

    # Construct model
    middle_layer = tf.layers.dense(inputs=input_type, units=num_hidden_1, activation=tf.nn.sigmoid, name="Hidden_Layer")
    network = tf.layers.dense(inputs=middle_layer, units=num_outputs, activation=tf.nn.sigmoid, name="Output_Layer")

    # Define cost and optimizer
    cost_computation = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=network, labels=output_type), name="Train_Cost")
    trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost_computation, name="Cost_Minimizer")

    # Train the model
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())  # randomly initialize network

        print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "before")
        print_manual_evaluation(session, network, input_type)

        # TODO Start Special Code
        tf.summary.scalar("cross_entropy_cost_summary", cost_computation)
        tf.summary.histogram("output_summary", network)
        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter("tensorboard", session.graph)
        # to run tensorboard, in a cmd window:
        # cd to the tensorboard directory (next to this file)
        # run: tensorboard --logdir=%CD%
        # look at command prompt to get browser url

        # notable:
        # https://github.com/tensorflow/tensorboard/issues/952
        # https://stackoverflow.com/questions/33772833/error-while-merging-summaries-for-tensorboard
        # https://stackoverflow.com/questions/41066244/tensorflow-module-object-has-no-attribute-scalar-summary
        # TODO End Special Code

        print("Training.")
        for i in range(total_training_sessions):  # _ just means ignore this value
            # fetches determines what to "compute"
            # passing trainer implies you want to compute, and therefor influence, the values of the network
            # TODO Start Special Code
            summary, _ = session.run(fetches=[merged, trainer], feed_dict={input_type: input_data_full, output_type: output_data_full})
            train_writer.add_summary(summary, i)
        # TODO End Special Code

        print_accuracy(session, network, input_data_full, output_data_full, input_type, output_type, "after")
        print_manual_evaluation(session, network, input_type)


run()
