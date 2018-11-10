import numpy as np

from custom.sc2bot_v1.GameAnalyst import GameAnalyst


class DecisionMaker:
	game_analyst = GameAnalyst()

	def get_target_tuple(self, game_analyst, current_values):
		target_values = np.zeros(4)
		old_score = 0

		# try different investment strategies
		for i in range(4):
			investment_strategy = np.copy(current_values)
			investment_strategy[i] = 400
			score = game_analyst.get_score(investment_strategy)

			# pick the best investment of the resources
			if score > old_score:
				target_values = investment_strategy

		return target_values
