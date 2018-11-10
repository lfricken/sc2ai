import math

from custom.sc2bot_v1.Investments import Investments


class GameAnalyst:

	def get_score(self, investment: Investments) -> int:
		worker_count = investment.worker / 50
		expand_count = investment.expand / 400

		# is expanding good?
		expand_weight = 400 * 1.5 * math.sqrt(expand_count)  # likes to expand to 2, not 3

		# is army good?
		army_weight = investment.army  # values army

		# are worker good?
		supported_expands = worker_count / 16
		if supported_expands < expand_count:
			worker_weight = investment.worker * 1.25  # we haven't saturated our expand, so build more!
		else:
			worker_weight = investment.worker * 0.5  # devalue over producing worker

		# is more production good?
		target_production = expand_count * 600
		if target_production < investment.production:
			production_weight = investment.production * 1.25
		else:
			production_weight = investment.production * 0.5  # devalue over producing buildings

		return expand_weight + army_weight + worker_weight + production_weight
