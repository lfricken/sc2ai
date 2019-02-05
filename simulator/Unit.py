from enum import Enum
from Math import *

class Team(Enum):
	Red = 1
	Blue = 2


class Unit:
	"""Represents some unit."""

	def __init__(self):
		self._health = 0  # If we have 0 health we die.
		self._max_range = 0
		self._min_range = 0
		self._speed = 0
		self._dps = 0
		self._can_shoot = True  # True if we can shoot this step. False because maybe we moved?
		self._does_aoe = False  # True if this unit does aoe damage.
		self._position: VectorInt = VectorInt(-999, -999)  # current position
		self._size = 0  # amount of a single sc2 cell we take up
		self.ignores_cliffs = False  # True if we can move over cliffs.
		self.has_air_movement_type = False  # True if we can move anywhere.
		self.has_air_vision_type = False  # True if we can see over cliffs.
		self.team: Team = Team.Red
		self.aoe_dps = 0  # dps done to all 4 adjacent cells

	@property
	def alive(self) -> bool:
		"""Returns true if this unit is alive."""
		return self.health >= 0

	@property
	def position(self) -> VectorInt:
		"""True if this unit can shoot this step."""
		return self._position

	@position.setter
	def position(self, value: VectorInt):
		"""True if this unit can shoot this step."""
		self._position = value

	@property
	def can_shoot(self) -> bool:
		"""True if this unit can shoot this step."""
		return self._can_shoot

	@can_shoot.setter
	def can_shoot(self, value: bool):
		"""True if this unit can shoot this step."""
		self._can_shoot = value

	@property
	def speed(self) -> float:
		"""How many game units per second."""
		return self._speed

	@speed.setter
	def speed(self, value: float):
		"""How many game units per second."""
		self._speed = value

	@property
	def size(self) -> float:
		"""Percentage of a 2x2 cell taken by this unit."""
		return self._size

	@size.setter
	def size(self, value: float):
		"""Percentage of a 2x2 cell taken by this unit."""
		self._size = value

	@property
	def does_aoe(self) -> bool:
		"""True if this unit does any AOE damage. Will apply normal dps to original cell"""
		return self._does_aoe

	@does_aoe.setter
	def does_aoe(self, value: bool):
		"""True if this unit does any AOE damage. Will apply normal dps to original cell"""
		self._does_aoe = value

	@property
	def dps(self) -> float:
		"""Damage applied per second."""
		return self._dps

	@dps.setter
	def dps(self, value: float):
		"""Damage applied per second."""
		self._dps = value

	@property
	def max_range(self) -> float:
		"""How many cells can this unit shoot."""
		return self._max_range

	@max_range.setter
	def max_range(self, value: float):
		"""How many cells can this unit shoot."""
		self._max_range = value

	@property
	def min_range(self) -> float:
		"""How many units can this unit shoot."""
		return self._min_range

	@min_range.setter
	def min_range(self, value: float):
		"""How many units can this unit shoot."""
		self._min_range = value

	@property
	def health(self) -> float:
		"""Health of this unit."""
		return self._health

	@health.setter
	def health(self, value: float):
		"""Health of this unit."""
		self._health = value
