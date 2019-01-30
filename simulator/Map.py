from Unit import *


class Cell:
	"""Holds units."""

	def add_unit(self, unit: Unit):
		self._space_taken += unit.size
		self._units[unit.team].append(unit)

	def remove_unit(self, unit: Unit):
		self._space_taken -= unit.size
		self._units[unit.team].remove(unit)

	def contains_team(self, team: Team) -> bool:
		"""Returns true if this cell contains units from that team."""
		return len(self._units[team]) > 0

	@property
	def get_units(self) -> {Team: [Unit]}:
		"""How much of this cell is taken up already."""
		return self._units

	@staticmethod
	def get_cell_size() -> int:
		"""How big is a cell in this map vs normal sc2?"""
		return 2

	@staticmethod
	def _get_cell_space() -> int:
		"""How much stuff can a cell hold?"""
		return Cell.get_cell_size() * Cell.get_cell_size()

	def __init__(self):
		self._space_taken = 0.0
		self._units: {Team: [Unit]} = {Team.Blue: [], Team.Red: []}
		self.raised = False
		self.cliff = False
		self.void = False

	raised: bool
	"""True if we can move over cliffs."""
	"""Ramps are merely raised terrain that joins with lower terrain without impassable."""

	cliff: bool
	"""This is a cliff."""

	void: bool
	"""This is void (only air units can go here)."""

	def will_fit(self, unit: Unit) -> bool:
		"""Returns true if this unit will fit in this cell."""
		return (self._space_taken + unit.size) <= Cell._get_cell_space()

	@property
	def space_taken(self) -> float:
		"""How much of this cell is taken up already."""
		return self._space_taken

	@space_taken.setter
	def space_taken(self, value: float):
		"""How much of this cell is taken up already."""
		self._space_taken = value


class Map:
	"""Map as a grid of cells."""

	def __init__(self, size: (int, int)):

		# fill grid with new cells
		self.grid: [[Cell]] = []
		for i in range(size[0]):
			self.grid.append([])
			for j in range(size[1]):
				self.grid[i].append(Cell())
