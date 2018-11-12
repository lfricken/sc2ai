from custom.sc2bot_v2.Investments import Investments


class DecisionMaker:
	"""
	Decides how to invest money.
	"""

	def get_target_values(self, heuristic, current_investments: Investments):
		"""
		What should our current investments look like? Adds some value onto our current set of investments.
		:param heuristic: Tells us whether an investment strategy is good or not.
		:param current_investments: Current investments. If we have 1 Barracks, production would be 150.
		:return: What our total investments should be.
		"""
		target_values = Investments()
		old_score = -1

		# try different investment strategies
		for index in range(Investments.num_investment_options()):
			new_strategy = self.generate_new_strategy(index, current_investments)
			score = heuristic.get_score(new_strategy)

			# pick the best investment option
			if score > old_score:
				old_score = score
				target_values = new_strategy

		return target_values

	def generate_new_strategy(self, index: int, current_investments: Investments) -> Investments:
		"""Think of a new way of investing the extra money."""
		additional_investment = Investments()
		additional_investment._investments[index] = Investments.investment_amount()

		return current_investments.plus(additional_investment)
