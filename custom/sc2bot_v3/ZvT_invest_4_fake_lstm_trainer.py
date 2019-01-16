# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

import random

from ZvT_invest_4_fake_lstm_vars import *

learning_rate = 0.1
training_epochs = 10
batch_size = 40

np.set_printoptions(precision=2)


def randomize_data(data_array):
	np.random.shuffle(data_array)


def generate_data() -> ([[int]], [[int]], [[int]], [[int]]):
	training_data_array: [Point] = []

	for training_data in TrainingValues.get_training_enumerable():
		extract_data(training_data, training_data_array)

	randomize_data(training_data_array)
	return format_data(training_data_array)


formatter = "%.2f"


def print_manual_evaluation(session: tf.Session, network, input_type: tf.placeholder, test_input: [[int]], test_answer: [[int]]):
	# by just passing network, it implies we want the output from network
	test_output: [[[int]]] = session.run(fetches=[network], feed_dict={input_type: test_input})
	case = random.randint(0, len(test_input))
	test_output = test_output[0][case]
	test_input = test_input[case]
	test_answer = test_answer[case]

	display_input = [formatter % member for member in test_input]
	display_output = test_output.tolist()
	display_output = [formatter % member for member in display_output]
	display_answer = [formatter % member for member in test_answer]

	print("Input: {}".format(display_input))
	print("Output:{}".format(display_output))
	print("Answer:{}".format(display_answer))


def print_accuracy(session, network, input_data, output_data, input_type, output_type, before_or_after):
	cost_computation = tf.losses.mean_squared_error(predictions=network, labels=output_type)
	cost = session.run(fetches=[cost_computation], feed_dict={input_type: input_data, output_type: output_data})
	print("Error {}: {:.3f}".format(before_or_after, cost[0]))


def run():
	(train_input, train_output, test_input, test_output) = generate_data()

	class_sums = [sum(x) for x in zip(*train_output)]
	for i in range(len(class_sums)):
		class_sums[i] /= len(train_output)
	display_answer = ["{:0.2f}".format(member) for member in class_sums]
	print("Class Distribution: {}".format(display_answer))

	# tf Graph input
	input_type, network, output_type = build_network()

	# Define loss and optimizer
	cost_computation = tf.losses.mean_squared_error(predictions=network, labels=output_type)
	trainer = tf.train.AdamOptimizer(learning_rate).minimize(cost_computation)

	saver = tf.train.Saver()
	with tf.Session() as session:
		session.run(tf.global_variables_initializer())

		# try to load the brain
		try:
			saver.restore(session, save_directory)
			print("Brain loaded.")  # We loaded a network!
		except ValueError:
			print("No brain found. Creating new brain.")  # There was nothing to load.

		print("")
		print_accuracy(session, network, train_input, train_output, input_type, output_type, "on train before")
		print_accuracy(session, network, test_input, test_output, input_type, output_type, "on test before")
		print_manual_evaluation(session, network, input_type, test_input, test_output)

		# tensorboard
		tf.summary.scalar("cross_entropy_cost_summary", cost_computation)
		tf.summary.histogram("output_summary", network)
		merged = tf.summary.merge_all()
		train_writer = tf.summary.FileWriter(tensorboard_dir, session.graph)

		print("")
		print("Training.")

		num_samples = len(train_input)
		num_batches = num_samples // batch_size

		total_count = 0

		for epoch in range(training_epochs):
			avg_cost = 0

			# batches should actually not be all the data
			batch_begin = 0
			for batch in range(num_batches):
				batch_end = batch_begin + batch_size
				summary, t = session.run(fetches=[merged, trainer], feed_dict={input_type: train_input[batch_begin:batch_end], output_type: train_output[batch_begin:batch_end]})

				train_writer.add_summary(summary, total_count)
				total_count += 1

			if epoch % 10 == 0:
				print("")
				print("Epoch {} Cost: {}".format(epoch, avg_cost))
				print_accuracy(session, network, train_input, train_output, input_type, output_type, "on training after")
				print_accuracy(session, network, test_input, test_output, input_type, output_type, "on test after")
				print_manual_evaluation(session, network, input_type, test_input, test_output)

		print("")
		print("Saving.")
		saver.save(session, save_directory)


run()
