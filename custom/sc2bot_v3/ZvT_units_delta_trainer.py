# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

import random

from ZvT_units_delta_vars import *

learning_rate = 10
training_epochs = 200
batch_size = 10

np.set_printoptions(precision=2)


def randomize_data(data_array):
	np.random.shuffle(data_array)


def generate_data() -> ([[int]], [[int]], [[int]], [[int]]):
	training_data_array: [Point] = []

	for training_data in TrainingValues.get_training_enumerable():
		new_data = extract_data(training_data)
		training_data_array.extend(new_data)

	return training_data_array


formatter = "%.4f"


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
	accuracy = tf.equal(tf.argmax(network), tf.argmax(output_type))
	accuracy = tf.reduce_mean(tf.cast(accuracy, "float"))
	calculated_accuracy = session.run(fetches=[accuracy], feed_dict={input_type: input_data, output_type: output_data})
	print("Accuracy {}: {:.2f}%".format(before_or_after, calculated_accuracy[0] * 100))


def run():
	training_data_array = generate_data()
	randomize_data(training_data_array)
	(train_input, train_output, test_input, test_output) = format_data(training_data_array)

	# input_norm = Normalizer(train_input, 0, 2)
	# train_input = input_norm.normalize_data(train_input)

	# output_norm = Normalizer(train_output, 0, 2)
	# train_output = output_norm.normalize_data(train_output)

	class_sums = [sum(x) for x in zip(*train_output)]
	for i in range(len(class_sums)):
		class_sums[i] /= len(train_output)
	display_answer = ["{:0.2f}".format(member) for member in class_sums]
	print("Class Distribution: {}".format(display_answer))

	# tf Graph input
	input_type, network, output_type = build_network(True)

	# Define loss and optimizer

	regularizer = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
	reg_losses = tf.reduce_sum(regularizer)

	error_init = tf.nn.softmax_cross_entropy_with_logits_v2(logits=network, labels=output_type)
	error = tf.reduce_mean(error_init)

	cost_computation = error  # tf.add(error, reg_losses)
	trainer = tf.train.AdadeltaOptimizer(learning_rate).minimize(cost_computation)
	normalize_op = tf.get_collection(tf.GraphKeys.UPDATE_OPS)

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
			randomize_data(training_data_array)
			(train_input, train_output, test_input, test_output) = format_data(training_data_array)
			avg_cost = 0
			batch_begin = 0
			for batch in range(num_batches):
				batch_end = batch_begin + batch_size
				summary, t, _, cost = session.run(fetches=[merged, trainer, normalize_op, error_init],
				                                  feed_dict={input_type: train_input[batch_begin:batch_end], output_type: train_output[batch_begin:batch_end]})

				avg_cost += cost

				train_writer.add_summary(summary, total_count)
				total_count += 1
			avg_cost = avg_cost / num_batches
			print("Epoch {} Cost: {}".format(epoch, avg_cost))

		# if epoch % 10 == 0:
		#	print_accuracy(session, network, train_input, train_output, input_type, output_type, "on training after")
		#	print_accuracy(session, network, test_input, test_output, input_type, output_type, "on test after")
		#	print_manual_evaluation(session, network, input_type, test_input, test_output)

		print("")
		print("Saving.")
		saver.save(session, save_directory)


run()
# os.system("python C:\\dev\\sc2ai\\custom\\sc2bot_v3\\ZvT_invest_4_fake_lstm_tester.py")
