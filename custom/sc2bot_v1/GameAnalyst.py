import math


class GameAnalyst:

	def get_score(self, investment):
		army_value = investment[0]
		worker_value = investment[1]
		expand_value = investment[2]
		production_value = investment[3]
		worker_count = worker_value / 50
		expand_count = expand_value / 400

		# is expanding good?
		expand_weight = 400 * 1.5 * math.sqrt(expand_count)  # likes to expand to 2, not 3

		# is army good?
		army_weight = army_value  # values army

		# are workers good?
		supported_expands = worker_count / 16
		if supported_expands < expand_count:
			worker_weight = worker_value * 1.25  # we haven't saturated our expands, so build more!
		else:
			worker_weight = worker_value * 0.5  # devalue over producing workers

		# is more production good?
		target_production = expand_count * 600
		if target_production < production_value:
			production_weight = production_value * 1.25
		else:
			production_weight = production_value * 0.5  # devalue over producing buildings

		return expand_weight + army_weight + worker_weight + production_weight
