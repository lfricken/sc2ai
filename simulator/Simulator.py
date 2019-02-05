from scipy.spatial.distance import cdist
import numpy as np

from GenerateUnit import *


class Simulator:

	def __init__(self):
		self.map: Map = Map((10, 10))
		self.units: {Team: [Unit]} = {Team.Blue: [], Team.Red: []}

	def try_add_unit(self, unit_name: str, position: VectorInt, team: Team) -> bool:
		"""Returns true if the unit had space to be added."""

		unit = generate_type(unit_name)
		unit.team = team

		cell: Cell = self.map.grid[position.x][position.y]
		has_space = cell.will_fit(unit)

		if has_space:
			cell.add_unit(unit)
			unit.position = position
			self.units[unit.team].append(unit)

		return has_space

	def get_cell(self, position: VectorInt) -> Cell:
		return self.map.grid[position.x][position.y]

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
				if eunit.alive and cdist(np.array([[unit.position.x, unit.position.y]]), np.array([[eunit.position.x, eunit.position.y]])) * Cell.get_cell_size() < unit.max_range:
					eunit.health -= unit.dps * time
					break
		for unit in self.units[Team.Blue]:
			if not unit.can_shoot:
				break
			for eunit in self.units[Team.Red]:
				if eunit.alive and cdist(np.array([[unit.position.x, unit.position.y]]), np.array([[eunit.position.x, eunit.position.y]])) * Cell.get_cell_size() < unit.max_range:
					eunit.health -= unit.dps * time
					break

	def try_move_unit(self, unit: Unit, time_delta: float, destination: VectorInt) -> bool:
		"""True if the unit moved towards the destination."""
		moved = False
		max_move_dist = time_delta * (unit.speed / float(Cell.get_cell_size()))
		desired_movement = unit.position.to(destination)
		desired_dist = desired_movement.length()

		realistic_target_pos: VectorInt = destination
		if not desired_dist <= max_move_dist:
			realistic_target_pos: VectorInt = to_vector_int(desired_movement.scale_length(max_move_dist) + unit.position)

		# resolve crowding
		cell: Cell = self.get_cell(realistic_target_pos)

		if not cell.will_fit(unit):
			current_cell = self.get_cell(unit.position)
			current_cell.remove_unit(unit)
			for i in range(10):
				positions: [VectorInt] = self.get_closer_positions(unit.position, realistic_target_pos)
			# find a cell that will

		# if our new destination is further, do nothing!
		if realistic_target_pos.to(destination).length() > unit.position.to(destination).length()
			return False

		# move the unit


		return moved

	def



	def get_closer_positions(self, start: VectorInt, end: VectorInt, units: int = 1) -> [VectorInt]:
		"""Returns 3 closest positions to end from start's point of view."""
		positions: [VectorInt] = []

		direction = end.to(start).unit()
		left: Vector = direction.rotate_90()
		right: Vector = left.negate()

		direction *= units

		left_close = to_vector_int(end + direction + left)
		middle_close = to_vector_int(end + direction)
		right_close = to_vector_int(end + direction + right)

		positions.append(left_close)
		positions.append(middle_close)
		positions.append(right_close)

		return positions
