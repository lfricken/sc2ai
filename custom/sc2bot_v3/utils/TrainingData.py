from utils.PlayerData import PlayerData


class DataPoint:
	player_1: PlayerData
	player_2: PlayerData
	who_won: [int]

	def __init__(self, p_1, p_2, winner):
		self.player_1 = p_1
		self.player_2 = p_2
		self.outputs: [int] = winner


class TrainingData:
	""""""

	data_points: [DataPoint] = None

	def __init__(self, player_1: PlayerData, player_2: PlayerData):
		self.data_points: [DataPoint] = []

		for increment in range(len(player_1.value_over_time)):
			output = [player_1.won_the_game, player_2.won_the_game]
			data = DataPoint(player_1, player_2, output)
			self.data_points.append(data)
