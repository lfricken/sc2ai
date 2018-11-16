from sc2reader.data import Unit

from custom.sc2bot_v2.Investments import Investments


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


def is_town_hall(unit: Unit) -> bool:
	if unit.title == "CommandCenter":
		return True
	if unit.title == "OrbitalCommand":
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


def is_production_building(unit: Unit) -> bool:
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

	if unit.title == "Hatchery":
		return True
	if unit.title == "Lair":
		return True
	if unit.title == "Hive":
		return True


def get_time_delta(increment: int) -> int:
	"""Use 5 second increments."""
	return 112 * increment  # 22.4 frames per second * 5seconds


def is_existing_army(unit: Unit, current_frame):
	return unit.is_army and unit_exists(unit, current_frame)


def is_existing_worker(unit: Unit, current_frame):
	return unit.is_worker and unit_exists(unit, current_frame)


class PlayerData:
	"""
	Contains data about this player over the course of the game.
	Used for a neural network to train on successful investment strategies.
	"""

	expand_value = [Investments]
	"""How much money in expands do we have at a given time."""

	total_frames: int = 0

	def __init__(self, player, total_frames: int):
		self.army_value = [int]
		self.total_frames = total_frames
		self.set_army_values(player, )

	def set_value_array(self, player, evaluator, array):
		self.army_value = [int]
		increment = 0
		current_frame = 0
		while current_frame < self.total_frames:
			for _ in player.units:
				unit: Unit = _
				if is_existing_army(unit, current_frame):
					total_frame_value += unit.minerals + unit.vespene
				if is_existing_worker(unit, current_frame):
					total_frame_value += unit.minerals + unit.vespene
			self.army_value.append(total_frame_value)

			increment += 1
			current_frame = get_time_delta(increment)

	def set_army_values(self, player):
		self.army_value = [int]
		current_frame = 0
		while current_frame < self.total_frames:
			total_frame_value = 0
			for _ in player.units:
				unit: Unit = _
				if unit.is_army and unit_exists(unit, current_frame):
					total_frame_value += unit.minerals + unit.vespene
			self.army_value.append(total_frame_value)
			current_frame += get_time_delta()

	def set_army_values(self, player):
		self.army_value = [int]
		current_frame = 0
		while current_frame < self.total_frames:
			total_frame_value = 0
			for _ in player.units:
				unit: Unit = _
				if unit.is_army and unit_exists(unit, current_frame):
					total_frame_value += unit.minerals + unit.vespene
			self.army_value.append(total_frame_value)
			current_frame += get_time_delta()

	def set_worker_values(self, player):
		self.army_value = [int]
		current_frame = 0
		while current_frame < self.total_frames:
			total_frame_value = 0
			for _ in player.units:
				unit: Unit = _
				if unit.is_worker and unit_exists(unit, current_frame):
					total_frame_value += unit.minerals + unit.vespene
			self.worker_value.append(total_frame_value)
			current_frame += get_time_delta()
