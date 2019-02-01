from Unit import *


class TerrainFlags(Enum):
	cliff = 1
	void = 2
	raised = 4
	filled = 8


class Map:
	"""Map as a grid of cells."""

	def __init__(self, size: (int, int)):
		# fill grid with new cells
		self.grid: [bytearray] = []
		for i in range(size[0]):
			self.grid.append(bytearray(size[1]))

	def set_type(self, position: (int, int), terrain_type: TerrainFlags):
		self.grid[position[0]][position[1]] |= terrain_type

	def unfill(self, position: (int, int)):
		self.grid[position[0]][position[1]] = self.grid[position[0]][position[1]] & (TerrainFlags.cliff | TerrainFlags.void | TerrainFlags.raised)

	def is_type(self, position: (int, int), terrain_type: TerrainFlags) -> bool:
		return bool(self.grid[position[0]][position[1]] | terrain_type)
