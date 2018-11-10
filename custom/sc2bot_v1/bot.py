import sc2
from sc2 import Difficulty
from sc2.constants import AbilityId as Ability
from sc2.constants import UnitTypeId as Unit
from sc2.game_data import *
from sc2.player import Bot, Computer

from custom.sc2bot_v1.DecisionMaker import DecisionMaker
from custom.sc2bot_v1.DecisionTaker import DecisionTaker
from custom.sc2bot_v1.GameAnalyst import GameAnalyst
from custom.sc2bot_v1.ValueCalculator import ValueCalculator
from custom.sc2bot_v1.Investments import Investments


class RampWallBot(sc2.BotAI):
	game_analyst: GameAnalyst = None
	decision_maker: DecisionMaker = None
	decision_taker: DecisionTaker = None
	value_calculator: ValueCalculator = None

	async def on_step(self, iteration):
		if iteration == 0:
			self.initialize()

		#if self.minerals > Investments.investment_threshold():
		self.macro()

		cc = self.units(Unit.COMMANDCENTER)
		if not cc.exists:
			return
		else:
			cc = cc.first

		if self.can_afford(Unit.SCV) and self.workers.amount < 16 and cc.noqueue:
			await self.do(cc.train(Unit.SCV))

		# Raise depots when enemies are nearby
		for depot in self.units(Unit.SUPPLYDEPOT).ready:
			for unit in self.known_enemy_units.not_structure:
				if unit.position.to2.distance_to(depot.position.to2) < 15:
					break
			else:
				await self.do(depot(Ability.MORPH_SUPPLYDEPOT_LOWER))

		# Lower depos when no enemies are nearby
		for depo in self.units(Unit.SUPPLYDEPOTLOWERED).ready:
			for unit in self.known_enemy_units.not_structure:
				if unit.position.to2.distance_to(depo.position.to2) < 10:
					await self.do(depo(Ability.MORPH_SUPPLYDEPOT_RAISE))
					break

		depot_placement_positions = self.main_base_ramp.corner_depots
		# Uncomment the following if you want to build 3 supplydepots in the wall instead of a barracks in the middle
		#  + 2 depots in the corner
		# depot_placement_positions = self.main_base_ramp.corner_depots | {self.main_base_ramp.depot_in_middle}

		barracks_placement_position = self.main_base_ramp.barracks_correct_placement
		# If you prefer to have the barracks in the middle without room for addons, use the following instead
		# barracks_placement_position = self.main_base_ramp.barracks_in_middle

		depots = self.units(Unit.SUPPLYDEPOT) | self.units(Unit.SUPPLYDEPOTLOWERED)

		# Filter locations close to finished supply depots
		if depots:
			depot_placement_positions = {d for d in depot_placement_positions if depots.closest_distance_to(d) > 1}

		# Build depots
		if self.can_afford(Unit.SUPPLYDEPOT) and not self.already_pending(Unit.SUPPLYDEPOT):
			if len(depot_placement_positions) == 0:
				return
			# Choose any depot location
			target_depot_location = depot_placement_positions.pop()
			ws = self.workers.gathering
			if ws:  # if worker were found
				w = ws.random
				await self.do(w.build(Unit.SUPPLYDEPOT, target_depot_location))

		# Build barracks
		if depots.ready.exists and self.can_afford(Unit.BARRACKS) and not self.already_pending(Unit.BARRACKS):
			if self.units(Unit.BARRACKS).amount + self.already_pending(Unit.BARRACKS) > 0:
				return
			ws = self.workers.gathering
			if ws and barracks_placement_position:  # if worker were found
				w = ws.random
				await self.do(w.build(Unit.BARRACKS, barracks_placement_position))

	def initialize(self):
		self.game_analyst = GameAnalyst()
		self.decision_maker = DecisionMaker()
		self.decision_taker = DecisionTaker()

		self.value_calculator = ValueCalculator(self)
		return

	def macro(self):
		# compute current investments
		investments = self.value_calculator.get_current_investments()

		# how much should we have invested in each area?
		target_investments = self.decision_maker.get_target_values(self.game_analyst, investments)

		self.decision_taker.do_action(target_investments)
		return


def main():
	sc2.run_game(sc2.maps.get("OdysseyLE"), [
		Bot(Race.Terran, RampWallBot()),
		Computer(Race.Zerg, Difficulty.Easy)
	], realtime=False)


if __name__ == '__main__':
	main()
