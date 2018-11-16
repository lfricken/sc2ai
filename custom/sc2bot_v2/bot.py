import sc2
from sc2 import Difficulty
from sc2.constants import AbilityId as Ability
from sc2.constants import UnitTypeId as UnitType
from sc2.game_data import *
from sc2.player import Bot, Computer
from sc2.unit import Unit

from DecisionMaker import DecisionMaker
from DecisionTaker import DecisionTaker
from GameAnalyst import GameAnalyst
from Investments import Investments
from Tactician import Tactician
from ValueCalculator import ValueCalculator


class BotV2(sc2.BotAI):
	game_analyst: GameAnalyst = None
	decision_maker: DecisionMaker = None
	decision_taker: DecisionTaker = None
	value_calculator: ValueCalculator = None
	tactician: Tactician = None

	target_investments: Investments = None

	async def on_step(self, iteration):
		if iteration == 0:
			self.initialize()
			return

		# grab a town hall without max workers
		town_hall = None
		town_hall_needs_workers = None
		for _ in self.units(UnitType.COMMANDCENTER).ready:
			cc: Unit = _
			town_hall = cc
			if cc.assigned_harvesters < cc.ideal_harvesters:
				town_hall_needs_workers = cc

		# reassign workers on mineral fields
		for _ in self.units(UnitType.COMMANDCENTER).ready:
			cc: Unit = _
			if cc.assigned_harvesters > cc.ideal_harvesters:
				worker = self.units(UnitType.SCV).ready.closest_to(cc.position)
				if town_hall_needs_workers:
					await self.do(worker.gather(self.state.mineral_field.closest_to(town_hall_needs_workers)))

		# assign idle workers
		_workers = self.units(UnitType.SCV).ready.idle
		for _ in _workers:
			worker: Unit = _
			if town_hall_needs_workers:
				await self.do(worker.gather(self.state.mineral_field.closest_to(town_hall_needs_workers)))

		# if self.minerals > Investments.investment_threshold():
		await self.macro()
		await self.micro()

		depot_placement_positions = self.main_base_ramp.corner_depots
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

		# build initial depots
		if self.can_afford(UnitType.SUPPLYDEPOT) and not self.already_pending(UnitType.SUPPLYDEPOT):
			if len(depot_placement_positions) != 0:
				# Choose any depot location
				target_depot_location = depot_placement_positions.pop()
				ws = self.workers.gathering
				if ws:  # if worker were found
					w = ws.random
					await self.do(w.build(UnitType.SUPPLYDEPOT, target_depot_location))

		# build subsequent depots
		if self.units(UnitType.SUPPLYDEPOT).ready and self.supply_left < 4:
			if self.can_afford(UnitType.SUPPLYDEPOT) and not self.already_pending(UnitType.SUPPLYDEPOT) and town_hall:
				await self.build(UnitType.SUPPLYDEPOT, near=town_hall.position.towards(self.game_info.map_center, 8))

	def initialize(self):
		self.game_analyst = GameAnalyst()
		self.decision_maker = DecisionMaker()
		self.decision_taker = DecisionTaker(self)
		self.value_calculator = ValueCalculator(self)
		self.tactician = Tactician(self)
		self.target_investments = Investments()
		return

	async def macro(self):
		# compute current investments
		investments = self.value_calculator.get_current_investments()

		investments_satisfied = self.target_investments.is_less_than_or_equal_to(investments)

		# how much should we have invested in each area?
		if investments_satisfied:
			self.target_investments = self.decision_maker.get_target_values(self.game_analyst, investments)

		await self.decision_taker.do_action(self.target_investments, investments)

	async def micro(self):
		await self.tactician.update()


def main():
	sc2.run_game(sc2.maps.get("OdysseyLE"), [
		Bot(Race.Terran, BotV2()),
		Computer(Race.Zerg, Difficulty.Easy)
	], realtime=False)


if __name__ == '__main__':
	main()
