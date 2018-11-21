import numpy as np

from utils.PlayerData import PlayerData


class DataPoint:
	inputs: [int] = None
	outputs: [int] = None

	def __init__(self, ins: [int], outs: [int]):
		self.inputs: [int] = ins
		self.outputs: [int] = outs


class TrainingData:
	""""""

	data_points: [DataPoint] = None

	def __init__(self, player_1: PlayerData, player_2: PlayerData):
		self.data_points: [DataPoint] = []

		for increment in range(len(player_1.value_over_time)):
			p1_investments: np.array = player_1.value_over_time[increment].investments
			p2_investments: np.array = player_2.value_over_time[increment].investments
			input_increment = np.concatenate([p1_investments, p2_investments])

			output = [player_1.won_the_game, player_2.won_the_game]

			data = DataPoint(input_increment, output)
			self.data_points.append(data)
