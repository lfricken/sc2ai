from Investments import Investments


class GameAnalyst:

	def get_score(self, investment: Investments) -> int:
		economy_calculation = min(investment.worker / 2.5, investment.expand)

		military_calculation = min(investment.army / 1, investment.production / 1)

		return min(economy_calculation, military_calculation)

	def default(self, value) -> int:
		if value == 0:
			return 1
		else:
			return value
