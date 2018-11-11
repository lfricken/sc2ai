from custom.sc2bot_v1.Investments import Investments


class GameAnalyst:

	def get_score(self, investment: Investments) -> int:
		worker_count = investment.worker / 50
		expand_count = investment.expand / 400

		economy_calculation = min(investment.worker / 2, investment.expand)

		military_calculation = min(investment.army / 1, min(investment.production, economy_calculation))

		return min(economy_calculation, military_calculation)

	def default(self, value) -> int:
		if value == 0:
			return 1
		else:
			return value
