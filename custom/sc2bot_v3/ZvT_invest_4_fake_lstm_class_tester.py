import matplotlib.pyplot as plt
import pandas as pd

from ZvT_invest_4_fake_lstm_class_vars import *

time_delta = get_time_delta_seconds()


class Network:
    session: tf.Session
    input_type: tf.placeholder
    network = None
    save_directory: str

    def __init__(self):
        self.save_directory = save_directory
        self.session = tf.Session()
        (self.input_type, self.network, _) = build_network(False)
        saver = tf.train.Saver()
        saver.restore(self.session, self.save_directory)

    def predict(self, input_data: [int]) -> [int]:
        output: [[[int]]] = self.session.run(fetches=[self.network], feed_dict={self.input_type: [input_data]})
        return output[0][0]


class PlotValues:
    label: str
    color: str
    style: str
    data: [int]
    plot: int
    xlabel: str
    ylabel: str

    def __init__(self, label, color, style, data, plot, xlabel, ylabel):
        self.label = label
        self.color = color
        self.style = style
        self.data = data
        self.plot = plot


def plot_data(lines: [PlotValues]):
    data = dict()
    data["x"] = np.arange(0, time_delta * len(lines[0].data), time_delta)
    for _ in lines:
        line: PlotValues = _
        data[line.label] = line.data

    df = pd.DataFrame(data)
    fig, ax = plt.subplots(nrows=3, ncols=1)

    for i in range(1, 2):
        ax[i].set_ylim([0, 1000])

    for _ in lines:
        line: PlotValues = _
        col = ax[line.plot]
        col.plot("x", line.label, data=df, marker="", color=line.color, linewidth=2, linestyle=line.style)
        col.legend()

        col.set_xlabel("Minutes")
        if line.plot == 0:
            col.set_ylabel("Actual Army Value")
        if line.plot == 1:
            col.set_ylabel("Predicted Investment Deltas")
        if line.plot == 2:
            col.set_ylabel("Actual Investment Deltas")


def run_test():
    network = Network()

    num_replays = 1
    start = 0
    min_replay = start
    max_replay = min_replay + num_replays

    count = 0
    for _ in FileEnumerable.get_analysis_enumerable():
        count += 1
        if count < min_replay:
            continue
        if count > max_replay:
            break

        training_data: TrainingData = _
        real1: [int] = []
        real2: [int] = []
        real3: [int] = []
        real4: [int] = []
        p1: [int] = []
        p2: [int] = []
        p3: [int] = []
        p4: [int] = []
        army1: [int] = []
        army2: [int] = []
        expand: [int] = []
        worker: [int] = []
        production: [int] = []

        training_data_array: [Point] = []
        extract_data(training_data, training_data_array)
        input_data_full, output_data_full, _, _ = format_data(training_data_array)

        for i in range(len(input_data_full)):
            input_data = input_data_full[i]
            output_data = output_data_full[i]

            prediction = network.predict(input_data)
            real1.append(output_data[0])
            real2.append(output_data[1])
            real3.append(output_data[2])
            real4.append(output_data[3])
            p1.append(prediction[0] * 1000)
            p2.append(prediction[1] * 1000)
            p3.append(prediction[2] * 1000)
            p4.append(prediction[3] * 1000)
            army1.append(input_data[0])
            army2.append(input_data[4])
        # expand.append(replay_data.us.core_values.expand)
        # worker.append(replay_data.us.core_values.worker)
        # production.append(replay_data.us.core_values.production)

        lines_to_plot: [PlotValues] = list()
        lines_to_plot.append(PlotValues("Zerg", "red", "-", army1, 0, "", ""))
        lines_to_plot.append(PlotValues("Enemy", "blue", "-", army2, 0, "", ""))
        lines_to_plot.append(PlotValues("Invest Army", "red", "-", p1, 1, "", ""))
        lines_to_plot.append(PlotValues("Invest Production", "blue", "-", p2, 1, "", ""))
        lines_to_plot.append(PlotValues("Invest Worker", "green", "-", p3, 1, "", ""))
        lines_to_plot.append(PlotValues("Invest Expand", "yellow", "-", p4, 1, "", ""))
        lines_to_plot.append(PlotValues("Invest Army2", "red", "-", real1, 2, "", ""))
        lines_to_plot.append(PlotValues("Invest Production2", "blue", "-", real2, 2, "", ""))
        lines_to_plot.append(PlotValues("Invest Worker2", "green", "-", real3, 2, "", ""))
        lines_to_plot.append(PlotValues("Invest Expand2", "yellow", "-", real4, 2, "", ""))
        # lines_to_plot.append(PlotValues("Production", "green", "--", production))
        # lines_to_plot.append(PlotValues("Expand", "olive", "--", expand))

        plot_data(lines_to_plot)
        plt.show()


run_test()
