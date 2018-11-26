from sc2reader.data import Unit

from utils.Investments import *


def unit_exists(unit: Unit, frame: int) -> bool:
	if unit.died_at is None:
		return unit.started_at <= frame
	else:
		if unit.started_at <= frame < unit.died_at:
			return True
		else:
			return False


def unit_started_during(unit: Unit, start_frame: int, end_frame: int) -> bool:
	if start_frame <= unit.started_at < end_frame:
		return True
	else:
		return False


def is_expand(unit: Unit) -> bool:
	if unit.title == "CommandCenter":
		return True
	if unit.title == "CommandCenterFlying":
		return True
	if unit.title == "OrbitalCommand":
		return True
	if unit.title == "OrbitalCommandFlying":
		return True
	if unit.title == "PlanetaryFortress":
		return True

	if unit.title == "Nexus":
		return True

	if unit.title == "Hatchery":
		return True
	if unit.title == "Lair":
		return True
	if unit.title == "Hive":
		return True


def is_production(unit: Unit) -> bool:
	if unit.title == "Barracks":
		return True
	if unit.title == "Factory":
		return True
	if unit.title == "Starport":
		return True
	if unit.title == "BarracksReactor":
		return True
	if unit.title == "FactoryReactor":
		return True
	if unit.title == "StarportReactor":
		return True

	if unit.title == "Gateway":
		return True
	if unit.title == "WarpGate":
		return True
	if unit.title == "RoboticsFacility":
		return True
	if unit.title == "Stargate":
		return True

	if unit.title == "SpawningPool":
		return True
	if unit.title == "RoachWarren":
		return True
	if unit.title == "BanelingNest":
		return True
	if unit.title == "HydraliskDen":
		return True
	if unit.title == "Spire":
		return True
	if unit.title == "InfestationPit":
		return True
	if unit.title == "UltraliskCavern":
		return True
	if unit.title == "GreaterSpire":
		return True


def get_time_delta() -> int:
	"""Use 5 second increments."""
	return 112  # 22.4 frames per second * 5seconds


def get_time_sample(increment: int) -> int:
	"""Use 5 second increments."""
	return get_time_delta() * increment


def is_army(unit: Unit):
	if unit.name == "Overlord" or unit.name == "OverseerCocoon" or unit.name == "Overseer":
		return False
	else:
		return unit.is_army


def is_worker(unit: Unit):
	return unit.is_worker


def unit_value(unit: Unit):
	return unit.minerals + unit.vespene


def get_unit_name(unit: Unit, current_frame: int) -> str:
	name: str = ""
	for start, data in unit.type_history.items():
		if start <= current_frame:
			name = data.name
	return name


class PlayerData:
	"""
	Contains data about this player over the course of the game.
	Used for a neural network to train on successful investment strategies.
	"""

	value_over_time = [Investments]
	"""We have money in these things during that time."""
	value_deltas = [Investments]
	"""We spent money on this during that time."""

	won_the_game: bool
	"""True if this player won the game."""
	total_frames: int = 0
	"""How many frames were in the whole game."""

	def __init__(self, vals):
		self.total_frames = vals.total_frames
		self.won_the_game = (vals.player.result == "Win")
		self.set_value_array(vals.player.units)

	def build_array(self):
		self.value_over_time: [Investments] = list()
		increment = 0
		current_frame = 0
		while current_frame < self.total_frames:
			current_frame = get_time_sample(increment)
			self.value_over_time.append(self.get_race_investment())
			increment += 1

		self.value_deltas: [Investments] = list()
		increment = 0
		current_frame = 0
		while current_frame < self.total_frames:
			current_frame = get_time_sample(increment)
			self.value_deltas.append(self.get_race_investment())
			increment += 1

	def set_value_array(self, units: [Unit]):
		self.build_array()
		for _ in units:
			unit: Unit = _

			if unit is None or unit.name is None:
				continue

			if ignore(unit.name):
				continue

			if not unit.is_army and not unit.is_worker and not unit.is_building:
				continue

			for start, values in unit.type_history.items():
				start_increment: int = start // get_time_delta()
				# ignore what we start with
				if start != 0:
					self.add_unit_count(self.value_deltas[start_increment], unit, start)

			tick_investments: Investments = self.get_race_investment()
			if is_army(unit):
				tick_investments.army += unit_value(unit)
			if is_worker(unit):
				tick_investments.worker += unit_value(unit)
			if is_expand(unit):
				tick_investments.expand += 400  # unit_value(unit)
			if is_production(unit):
				tick_investments.production += unit_value(unit)

			# process this unit over time
			increment: int = int(0)
			current_frame = 0
			while current_frame < self.total_frames:
				current_frame = get_time_sample(increment)

				if unit_exists(unit, current_frame):
					target_investments: Investments = self.value_over_time[increment]
					target_investments = target_investments.plus(tick_investments)

					if not self.add_unit_count(target_investments, unit, current_frame):
						break

					self.value_over_time[increment] = target_investments

				increment += 1

	def add_unit_count(self, target_investments: Investments, unit: Unit, current_frame) -> bool:
		unit_type: str = fix_name(get_unit_name(unit, current_frame).upper())
		if unit_type != "" and hasattr(target_investments, unit_type):
			setattr(target_investments, unit_type, getattr(target_investments, unit_type) + 1)
			return True
		else:
			return False

	def get_race_investment(self):
		ValueError("You called get_race_investment on the base class!")


class TerranData(PlayerData):
	value_over_time = [TerranInvestments]

	def __init__(self, vals):
		super(TerranData, self).__init__(vals)

	def get_race_investment(self) -> Investments:
		return TerranInvestments()


class ZergData(PlayerData):
	value_over_time = [ZergInvestments]

	def __init__(self, vals):
		super(ZergData, self).__init__(vals)

	def get_race_investment(self) -> Investments:
		return ZergInvestments()


class ProtossData(PlayerData):
	value_over_time = [ProtossInvestments]

	def __init__(self, vals):
		super(ProtossData, self).__init__(vals)

	def get_race_investment(self) -> Investments:
		return ProtossInvestments()
