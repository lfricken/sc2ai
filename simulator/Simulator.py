from scipy.spatial.distance import cdist
import numpy as np

from GenerateUnit import *


class TeamGlobals:

	def __init__(self):
		self.minerals = 0
		self.vespene = 0


class Simulator:

	def __init__(self):
		self.map: Map = Map((10, 10))
		self.units: {Team: [Unit]} = {Team.Blue: [], Team.Red: []}

	def try_add_unit(self, unit_name: str, position: (float, float), team: Team) -> bool:
		"""Returns true if the unit had space to be added."""

		unit = generate_type(unit_name)
		unit.team = team

		has_space = True  # cell.will_fit(unit)

		if has_space:
			unit.position = position
			self.units[unit.team].append(unit)

		return has_space

	def remove_dead(self):
		for unit in self.units[Team.Red]:
			if unit.health <= 0:
				self.units[Team.Red].remove(unit)
		for unit in self.units[Team.Blue]:
			if unit.health <= 0:
				self.units[Team.Red].remove(unit)

	def apply_attacks(self, time):
		return

	# for unit in self.units[Team.Red]:
	# 	if not unit.can_shoot:
	# 		break
	# 	for eunit in self.units[Team.Blue]:
	# 		if eunit.alive and cdist(np.array([[unit.position[0] * Cell.get_cell_size(), unit.position[1] * Cell.get_cell_size()]]),
	# 		                         np.array([[eunit.position[0] * Cell.get_cell_size(), eunit.position[1] * Cell.get_cell_size()]])) < unit.max_range:
	# 			eunit.health -= unit.dps * time
	# 			break
	# for unit in self.units[Team.Blue]:
	# 	if not unit.can_shoot:
	# 		break
	# 	for eunit in self.units[Team.Red]:
	# 		if eunit.alive and cdist(np.array([[unit.position[0] * Cell.get_cell_size(), unit.position[1] * Cell.get_cell_size()]]),
	# 		                         np.array([[eunit.position[0] * Cell.get_cell_size(), eunit.position[1] * Cell.get_cell_size()]])) < unit.max_range:
	# 			eunit.health -= unit.dps * time
	# 			break

	def already_moved(self):
		for unit in self.units[Team.Red]:
			unit.can_shoot = True
		for unit in self.units[Team.Blue]:
			unit.can_shoot = True

	# def try_moves(self, time):
	# for unit in self.units[Team.Red]:
	# 	if unit.destination is not None:
	# 		current_position = [unit.position[0] * Cell.get_cell_size(), unit.position[1] * Cell.get_cell_size()]
	# 		destination = [unit.destination[0] * Cell.get_cell_size(), unit.destination[1] * Cell.get_cell_size()]
	# 		unit.can_shoot = False
	# 		distance = cdist(np.array([current_position]), np.array([]))
	# 		move_distance = time * unit.speed
	# 		cell: Cell = self.get_cell(unit.destination)
	# 		if distance <= move_distance and cell.will_fit(unit):
	# 			self.move(unit)
	# 		else:
	# 			delta = np.subtract(destination, current_position)
	# 			delta *= move_distance / distance
	# 			new_position = np.add(current_position, delta)

	def compute_new_position(self, move_distance, destination) -> (float, float):
		return (0, 0)

	def move(self, unit: Unit):
		current_cell = self.get_cell(unit.position)
		current_cell.remove_unit(unit)
		next_cell = self.get_cell(unit.destination)
		next_cell.add_unit(unit)
