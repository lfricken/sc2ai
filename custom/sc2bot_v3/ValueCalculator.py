import sc2
from sc2.constants import AbilityId as Ability
from sc2.constants import UnitTypeId as Unit
from sc2.constants import UpgradeId as Upgrade
from sc2.game_data import *

from utils.Investments import Investments


class ValueCalculator:
	"""Tells you how many resources are invested into various things."""

	bot: sc2.BotAI = None
	"""Reference to our bot to grab game state data."""

	def __init__(self, bot: sc2.BotAI):
		self.bot = bot

	def get_current_investments(self) -> Investments:
		"""TODO: do we need to take into account pending buildings? Probably."""
		"""Returns current investments."""
		current_investments = Investments()
		current_investments = current_investments - current_investments
		current_investments.army = self.calc_army()
		current_investments.production = self.calc_production()
		current_investments.expand = self.calc_expands()
		current_investments.worker = self.calc_workers()

		return current_investments

	def calc_workers(self) -> int:
		count = 0

		count += self.calc_unit_sum(Unit.SCV)

		return count

	def calc_production(self) -> int:
		count = 0

		count += self.calc_unit_sum(Unit.BARRACKS)
		count += self.calc_unit_sum(Unit.BARRACKSREACTOR)
		count += self.calc_unit_sum(Unit.FACTORY)
		count += self.calc_unit_sum(Unit.FACTORYREACTOR)
		count += self.calc_unit_sum(Unit.STARPORT)
		count += self.calc_unit_sum(Unit.STARPORTREACTOR)

		return count

	def calc_army(self) -> int:
      # make this const
		unit_types = [Unit.MARINE]  # ...
		return sum([self.calc_unit_sum(u) for u in unit_types])

	def calc_expands(self) -> int:
		"""
		TODO: should this use the api to get expand count?
		https://github.com/Dentosal/python-sc2/wiki/The-BotAI-class
		"""
		expand_types = [Unit.COMMANDCENTER,
							 Unit.ORBITALCOMMAND,
							 Unit.PLANETARYFORTRESS]
		return sum([self.calc_unit_sum(e) for e in expand_types])

	def calc_unit_sum(self, thing) -> int:
		"""Get the total current resource investment in this unit type."""
		return sum([self.get_cost_sum(thing) for _ in self.bot.units(thing)])

	def get_cost_sum(self, item_id: Union[Unit, Upgrade, Ability]) -> int:
		"""
		Get the cost of a unit, upgrade, or ability by summing its minerals and vespene.
		:param bot: Bot that contains data.
		:param item_id: Thing to check cost for.
		:return: Total resource cost of a thing.
		"""
		value = self.get_cost(item_id)
		return value.minerals + value.vespene

	def get_cost(self, item_id: Union[Unit, Upgrade, Ability]) -> Cost:
		"""
		Get the cost a unit, upgrade, or ability.
		:param bot: Bot that contains data.
		:param item_id: Thing to check cost for.
		:return: Cost of thing in vespene and minerals.
		"""
		if isinstance(item_id, Unit):
			unit = self.bot._game_data.units[item_id.value]
			cost = self.bot._game_data.calculate_ability_cost(unit.creation_ability)
		elif isinstance(item_id, Upgrade):
			cost = self.bot._game_data.upgrades[item_id.value].cost
		else:
			cost = self.bot._game_data.calculate_ability_cost(item_id)

		return cost
