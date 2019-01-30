from scipy.spatial.distance import cdist
import numpy as np

from GenerateUnit import *


class Simulator:

	def __init__(self):
		self.map: Map = Map((10, 10))
		self.units: {Team: [Unit]} = {Team.Blue: [], Team.Red: []}

	def try_add_unit(self, unit_name: str, position: (float, float), team: Team) -> bool:
		"""Returns true if the unit had space to be added."""

		unit = generate_type(unit_name)
		unit.team = team

		cell: Cell = self.map.grid[position[0]][position[1]]
		has_space = cell.will_fit(unit)

		if has_space:
			cell.add_unit(unit)
			unit.position = position
			self.units[unit.team].append(unit)

		return has_space

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
			if not unit.can_shoot:
				break
			for eunit in self.units[Team.Blue]:
				if eunit.alive and cdist(np.array([[unit.position[0] * Cell.get_cell_size(), unit.position[1] * Cell.get_cell_size()]]), np.array([[eunit.position[0] * Cell.get_cell_size(), eunit.position[1] * Cell.get_cell_size()]])) < unit.max_range:
					eunit.health -= unit.dps * time
					break
		for unit in self.units[Team.Blue]:
			if not unit.can_shoot:
				break
			for eunit in self.units[Team.Red]:
				if eunit.alive and cdist(np.array([[unit.position[0] * Cell.get_cell_size(), unit.position[1] * Cell.get_cell_size()]]), np.array([[eunit.position[0] * Cell.get_cell_size(), eunit.position[1] * Cell.get_cell_size()]])) < unit.max_range:
					eunit.health -= unit.dps * time
					break
