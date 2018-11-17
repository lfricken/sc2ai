import numpy as np

from PlayerData import PlayerData


class TrainingData:
	""""""

	inputs: [np.array] = []
	outputs: [np.array] = []

	def __init__(self, player_1: PlayerData, player_2: PlayerData):
		did_player_2_win = player_2.won_the_game

		for increment in range(len(player_1.value_over_time)):
			p1_investments: np.array = player_1.value_over_time[increment].investments
			p2_investments: np.array = player_2.value_over_time[increment].investments
			input_increment = np.concatenate([p1_investments, p2_investments])
			self.inputs.append(input_increment)

			self.outputs.append(np.array([did_player_2_win]))
