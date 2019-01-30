from Map import *
from scipy.spatial.distance import cdist

from GenerateUnit import *
import numpy as np


class Simulator:

	def __init__(self):
		self.map: Map = Map((10, 10))
		self.units: {Team: [Unit]} = {Team.Blue: [], Team.Red: []}

	def try_add_unit(self, unit_name: str, position: (float, float), team: Team) -> bool:
		"""Returns true if the unit had space to be added."""

		unit = generate_type(unit_name)
		unit.team = team

		cell: Cell = self.map.grid[position[0]][position[1]]
		new_space = cell.space_taken + unit.size
		had_space = new_space <= cell.max_space_taken

		if had_space:
			cell.add_unit(unit)
			unit.position = position
			self.units[unit.team].append(unit)

		return had_space

	def get_cell(self, position: (float, float)) -> Cell:
		return self.map.grid[position[0]][position[1]]

	def remove_dead(self):
		for unit in self.units[Team.Red]:
			if unit.health <= 0:
				cell: Cell = self.get_cell(unit.position)
				cell.remove_unit(unit)
				self.units[Team.Red].remove(unit)
		for unit in self.units[Team.Blue]:
			if unit.health <= 0:
				cell: Cell = self.get_cell(unit.position)
				cell.remove_unit(unit)
				self.units[Team.Blue].remove(unit)

	def apply_attacks(self, time):
		for unit in self.units[Team.Red]:
			for eunit in self.units[Team.Blue]:
				if cdist(np.array([[unit.position[0], unit.position[1]]]), np.array([[eunit.position[0], eunit.position[1]]])) < unit.max_range:
					eunit.health -= unit.dps * time
					break
