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


def get_time_delta_seconds() -> int:
	return 5


def get_time_delta() -> int:
	"""Use 5 second increments."""
	return int(22.4 * get_time_delta_seconds())  # 22.4 frames per second


def get_frame(increment: int) -> int:
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


class DataPoint:
	core_values: Investments = None
	"""We spent money on this during that time."""
	unit_count: Investments = None
	"""We have money in these things during that time."""
	unit_count_deltas: Investments = None
	"""We spent money on this during that time."""
	
	"""Previous units built. Going up to five atm."""
	previous_built_units: Investments = None  # most recent previous unit

	def __init__(self, player_data):
		self.core_values: CoreInvestments = CoreInvestments()
		self.unit_count: Investments = player_data.get_race_investment()
		self.unit_count_deltas: Investments = player_data.get_race_investment()
		self.previous_built_units: Investments = player_data.get_race_investment()


class PlayerData:
	"""
	Contains data about this player over the course of the game.
	Used for a neural network to train on successful investment strategies.
	"""

	total_frames: int = 0
	"""How many frames were in the whole game."""
	won_the_game: bool
	"""True if this player won the game."""
	data: [DataPoint] = [DataPoint]
	""""""

	def __init__(self, vals):
		self.total_frames = vals.total_frames
		self.won_the_game: bool = (vals.player.result == "Win")

		if self.won_the_game:
			print(vals.player.play_race)

		self.data: [DataPoint] = []
		increment = 0
		current_frame = 0
		while current_frame < self.total_frames:
			self.data.append(DataPoint(self))
			increment += 1
			current_frame = get_frame(increment)

		self.set_value_array(vals.player.units)
		
		# calc prev built units
		prev_delta = self.data[0].unit_count_deltas
		for index in range(len(self.data)):
			curr_delta = self.data[index].unit_count_deltas
			if curr_delta.unit_was_built:
				prev_delta = curr_delta.units_built
			self.data[index].unit_count_deltas = prev_delta

	def set_value_array(self, units: [Unit]):
		for unit in units:

			if not unit or not unit.name:
				continue

			if ignore(unit.name):
				continue

			if not unit.is_army and not unit.is_worker and not unit.is_building:
				continue

			# deltas
			for start, values in unit.type_history.items():
				start_increment: int = start // get_time_delta()
				unit_count_deltas = self.data[start_increment].unit_count_deltas
				if start != 0:  # ignore what we start with
					self.add_unit_count(unit_count_deltas, unit, start)

			increment: int = int(0)
			current_frame = 0
			added = False
			while current_frame < self.total_frames:
				current_frame = get_frame(increment + 1)
				# because we check against current frame and not next frame, we actually check if a unit existed
				# at the beginning of this increment, and not th end
				if unit_exists(unit, current_frame):
					added = True

					# core
					core_values: CoreInvestments = self.data[increment].core_values
					self.add_core(unit, core_values)

					# counts
					unit_count: Investments = self.data[increment].unit_count
					additional_count: Investments = self.get_race_investment()
					if not self.add_unit_count(additional_count, unit, current_frame):
						break
					self.data[increment].unit_count = unit_count + additional_count

				elif added:  # it doesnt exist and it existed in the past
					break  # so we can stop

				increment += 1

	def add_unit_count(self, target_investments, unit: Unit, current_frame) -> bool:
		unit_type: str = fix_name(get_unit_name(unit, current_frame).upper())
		if unit_type != "" and hasattr(target_investments, unit_type):
			setattr(target_investments, unit_type, getattr(target_investments, unit_type) + 1)
			return True
		else:
			return False

	def add_core(self, unit: Unit, value_counts: CoreInvestments):
		if is_army(unit):
			value_counts.army += unit_value(unit)
		if is_worker(unit):
			value_counts.worker += unit_value(unit)
		if is_expand(unit):
			value_counts.expand += 400  # unit_value(unit)
		if is_production(unit):
			value_counts.production += unit_value(unit)

	def get_race_investment(self):
		ValueError("You called get_race_investment on the base class!")


class TerranData(PlayerData):

	def __init__(self, vals):
		super(TerranData, self).__init__(vals)

	def get_race_investment(self) -> TerranInvestments:
		return TerranInvestments()


class ZergData(PlayerData):

	def __init__(self, vals):
		super(ZergData, self).__init__(vals)

	def get_race_investment(self) -> ZergInvestments:
		return ZergInvestments()


class ProtossData(PlayerData):

	def __init__(self, vals):
		super(ProtossData, self).__init__(vals)

	def get_race_investment(self) -> ProtossInvestments:
		return ProtossInvestments()
