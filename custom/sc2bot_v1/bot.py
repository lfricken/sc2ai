import sc2
from sc2 import Difficulty
from sc2.constants import AbilityId as Ability
from sc2.constants import UnitTypeId as UnitType
from sc2.game_data import *
from sc2.player import Bot, Computer
from sc2.unit import Unit

from custom.sc2bot_v1.DecisionMaker import DecisionMaker
from custom.sc2bot_v1.DecisionTaker import DecisionTaker
from custom.sc2bot_v1.GameAnalyst import GameAnalyst
from custom.sc2bot_v1.ValueCalculator import ValueCalculator


class sc2bot_v1(sc2.BotAI):
	game_analyst: GameAnalyst = None
	decision_maker: DecisionMaker = None
	decision_taker: DecisionTaker = None
	value_calculator: ValueCalculator = None

	async def on_step(self, iteration):
		if iteration == 0:
			self.initialize()

		town_hall = (self.units(UnitType.COMMANDCENTER) | self.units(UnitType.ORBITALCOMMAND)).first

		# if self.minerals > Investments.investment_threshold():
		await self.macro()

		depot_placement_positions = self.main_base_ramp.corner_depots
		# Uncomment the following if you want to build 3 supplydepots in the wall instead of a barracks in the middle
		#  + 2 depots in the corner
		# depot_placement_positions = self.main_base_ramp.corner_depots | {self.main_base_ramp.depot_in_middle}

		barracks_placement_position = self.main_base_ramp.barracks_correct_placement
		# If you prefer to have the barracks in the middle without room for addons, use the following instead
		# barracks_placement_position = self.main_base_ramp.barracks_in_middle

		depots = self.units(UnitType.SUPPLYDEPOT) | self.units(UnitType.SUPPLYDEPOTLOWERED)

		# Filter locations close to finished supply depots
		if depots:
			depot_placement_positions = {d for d in depot_placement_positions if depots.closest_distance_to(d) > 1}

		for depot in self.units(UnitType.SUPPLYDEPOT).ready:
			for unit in self.known_enemy_units.not_structure:
				if unit.position.to2.distance_to(depot.position.to2) < 15:
					break
			else:
				await self.do(depot(Ability.MORPH_SUPPLYDEPOT_LOWER))

		# Lower depos when no enemies are nearby
		for depot in self.units(UnitType.SUPPLYDEPOTLOWERED).ready:
			for unit in self.known_enemy_units.not_structure:
				if unit.position.to2.distance_to(depot.position.to2) < 10:
					await self.do(depot(Ability.MORPH_SUPPLYDEPOT_RAISE))
					break

		if self.supply_left < 2:
			if self.can_afford(UnitType.SUPPLYDEPOT):
				await self.build(UnitType.SUPPLYDEPOT, near=town_hall.position.towards(self.game_info.map_center, 8))

		_workers = self.units(UnitType.SCV).idle
		for _ in _workers:
			worker: Unit = _
			await self.do(worker.gather(self.state.mineral_field.closest_to(town_hall)))

		# Build depots
		if self.can_afford(UnitType.SUPPLYDEPOT) and not self.already_pending(UnitType.SUPPLYDEPOT):
			if len(depot_placement_positions) == 0:
				return
			# Choose any depot location
			target_depot_location = depot_placement_positions.pop()
			ws = self.workers.gathering
			if ws:  # if worker were found
				w = ws.random
				await self.do(w.build(UnitType.SUPPLYDEPOT, target_depot_location))

	def initialize(self):
		self.game_analyst = GameAnalyst()
		self.decision_maker = DecisionMaker()
		self.decision_taker = DecisionTaker(self)
		self.value_calculator = ValueCalculator(self)
		return

	async def macro(self):
		# compute current investments
		investments = self.value_calculator.get_current_investments()

		# how much should we have invested in each area?
		target_investments = self.decision_maker.get_target_values(self.game_analyst, investments)

		await self.decision_taker.do_action(target_investments, investments)
		return


def main():
	sc2.run_game(sc2.maps.get("OdysseyLE"), [
		Bot(Race.Terran, sc2bot_v1()),
		Computer(Race.Zerg, Difficulty.Easy)
	], realtime=False)


if __name__ == '__main__':
	main()
