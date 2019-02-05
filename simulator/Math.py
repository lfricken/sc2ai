import math


class Vector:
	"""Represents a 2D vector."""

	def __init__(self, x: float = 0, y: float = 0):
		self.x = float(x)
		self.y = float(y)

	def __add__(self, val):
		return Vector(self.x + val.x, self.y + val.y)

	def __sub__(self, val):
		return Vector(self.x - val.x, self.y - val.y)

	def __iadd__(self, val):
		self.x = val.x + self.x
		self.y = val.y + self.y
		return self

	def __isub__(self, val):
		self.x = self.x - val.x
		self.y = self.y - val.y
		return self

	def __div__(self, val: float):
		return Vector(self.x / val, self.y / val)

	def __mul__(self, val):
		return Vector(self.x * val, self.y * val)

	def __idiv__(self, val):
		self.x = self.x / val
		self.y = self.y / val
		return self

	def __imul__(self, val):
		self.x = self.x * val
		self.y = self.y * val
		return self

	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def to(self, other: "Vector") -> "Vector":
		return other - self

	def distance_to(self, other: "Vector") -> float:
		return math.sqrt((self.x - other.x) ** 2 + (self.x - other.y) ** 2)

	def length(self) -> float:
		"""Returns the length of a vector."""
		return math.sqrt(self.length_sqrd())

	def project_onto(self, v: "Vector") -> "Vector":
		"""Projects self onto v."""
		return v.__mul__(self.dot(v) / self.length_sqrd())

	def length_sqrd(self) -> float:
		"""Returns the length of a vector squared. Faster than length(), but only marginally."""
		return self.x ** 2 + self.y ** 2

	def dot(self, other: "Vector") -> float:
		return self.x * other.x + self.y * other.y

	def unit(self):
		if self.x == 0 and self.y == 0:
			return Vector(0, 0)
		return self.__div__(self.length())

	def negate(self) -> "Vector":
		return Vector(-self.x, -self.y)

	def scale_length(self, new_length: float) -> "Vector":
		return self.unit() * new_length

	def rotate_90(self):
		return Vector(-self.y, self.x)


class VectorInt(Vector):

	def __init__(self, x: int = 0, y: int = 0):
		object.__init__(self)
		self.x = int(x)
		self.y = int(y)

	def to_float(self) -> Vector:
		return Vector(self.x, self.y)


def to_vector_int(other: Vector) -> VectorInt:
	return VectorInt(round(other.x), round(other.y))
