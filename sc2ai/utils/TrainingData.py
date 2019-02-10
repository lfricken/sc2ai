from sc2ai.utils.PlayerData import *


class CombinedDataPoint:
	us: DataPoint
	them: DataPoint
	who_won: [int]

	def __init__(self, us, them, winner):
		self.us = us
		self.them = them
		self.who_won = winner


class TrainingData:
	""""""

	data: [CombinedDataPoint]

	def __init__(self, us: PlayerData, them: PlayerData):
		self.data: [CombinedDataPoint] = []

		for increment in range(len(us.data)):
			us_point = us.data[increment]
			them_point = them.data[increment]
			winner = [us.won_the_game, them.won_the_game]

			data_point = CombinedDataPoint(us_point, them_point, winner)
			self.data.append(data_point)
