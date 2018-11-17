import numpy as np


class Investments:
	"""
	How many resources, and invested in what?
	"""

	@staticmethod
	def num_investment_options():
		"""
		How many investment variables do we consider?
		A.K.A. length of new_investment_array.
		"""
		return 4

	@staticmethod
	def investment_threshold():
		"""Amount of money we should have before deciding how to invest again."""
		return 200

	@staticmethod
	def investment_amount():
		"""Amount of money we should we consider investing each time."""
		return 400

	investments: np.ndarray = None

	def __init__(self):
		self.investments = np.full((Investments.num_investment_options()), 0)

	def plus(self, other: "Investments") -> "Investments":
		"""Add another investment to this one."""
		new_value = Investments()
		new_value.investments = np.add(self.investments, other.investments)

		return new_value

	def minus(self, other: "Investments") -> "Investments":
		"""Add another investment to this one."""
		new_value = Investments()
		new_value.investments = np.subtract(self.investments, other.investments)

		return new_value

	def is_less_than_or_equal_to(self, other: "Investments") -> bool:
		temp = other.minus(self)
		return (temp.investments >= 0).all()

	@property
	def army(self) -> int:
		"""Resources in military units."""
		return self.investments[0]

	@army.setter
	def army(self, value):
		self.investments[0] = value

	@property
	def production(self) -> int:
		"""Resources in production potential."""
		return self.investments[1]

	@production.setter
	def production(self, value):
		self.investments[1] = value

	@property
	def worker(self) -> int:
		"""Resources in worker units."""
		return self.investments[2]

	@worker.setter
	def worker(self, value):
		self.investments[2] = value

	@property
	def expand(self) -> int:
		"""Resources in town centers."""
		return self.investments[3]

	@expand.setter
	def expand(self, value):
		self.investments[3] = value
