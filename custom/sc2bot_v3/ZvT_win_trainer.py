# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

from __future__ import print_function

from ZvT_win_vars import *

learning_rate = 2
training_epochs = 500
batch_size = 40

np.set_printoptions(precision=2)


def randomize_data(data_array):
	np.random.shuffle(data_array)


def generate_data() -> ([[int]], [[int]], [[int]], [[int]]):
	training_data_array: [Point] = []

	for training_data in TrainingValues.get_training_enumerable():
		extract_data(training_data, training_data_array)

	return training_data_array


def print_accuracy(session, network, input_data, output_data, input_type, output_type, before_or_after):
	accuracy = tf.equal(tf.math.round(network), output_type)
	accuracy = tf.reduce_mean(tf.cast(accuracy, "float"))
	calculated_accuracy = session.run(fetches=[accuracy], feed_dict={input_type: input_data, output_type: output_data})
	print("Accuracy {}: {:.2f}%".format(before_or_after, calculated_accuracy[0] * 100))


def run():
	training_data_array = generate_data()
	randomize_data(training_data_array)
	(train_input, train_output, test_input, test_output) = format_data(training_data_array)

	input_norm = Normalizer(train_input, 0, 2)
	train_input = input_norm.normalize_data(train_input)
	test_input = input_norm.normalize_data(test_input)

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

	error = tf.losses.mean_squared_error(predictions=network, labels=output_type)

	cost_computation = tf.add(error, reg_losses)
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
		print_manual_evaluation(session, network, input_type, test_input)

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
			train_input = input_norm.normalize_data(train_input)
			avg_cost = 0
			batch_begin = 0
			for batch in range(num_batches):
				batch_end = batch_begin + batch_size
				summary, t, _, cost = session.run(fetches=[merged, trainer, normalize_op, cost_computation],
				                                  feed_dict={input_type: train_input[batch_begin:batch_end], output_type: train_output[batch_begin:batch_end]})

				avg_cost += cost

				train_writer.add_summary(summary, total_count)
				total_count += 1
			avg_cost = avg_cost / num_batches
			print("Epoch {} Cost: {}".format(epoch, avg_cost))

		print("")
		print_accuracy(session, network, train_input, train_output, input_type, output_type, "on train after")
		test_input = input_norm.normalize_data(test_input)
		print_accuracy(session, network, test_input, test_output, input_type, output_type, "on test after")
		print_manual_evaluation(session, network, input_type, test_input)

		print("")
		print("Saving.")
		saver.save(session, save_directory)


run()
# os.system("python C:\\dev\\sc2ai\\custom\\sc2bot_v3\\ZvT_invest_4_fake_lstm_tester.py")
