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

	_investments = None

	def __init__(self):
		self._investments = np.full((Investments.num_investment_options()), 1)

	def plus(self, other: "Investments") -> "Investments":
		"""Add another investment to this one."""
		new_value = Investments()
		new_value._investments = np.add(self._investments, other._investments)

		return new_value

	def minus(self, other: "Investments") -> "Investments":
		"""Add another investment to this one."""
		new_value = Investments()
		new_value._investments = np.subtract(self._investments, other._investments)

		return new_value

	@property
	def army(self):
		"""Resources in military units."""
		return self._investments[0]

	@army.setter
	def army(self, value):
		self._investments[0] = value

	@property
	def worker(self):
		"""Resources in worker units."""
		return self._investments[1]

	@worker.setter
	def worker(self, value):
		self._investments[1] = value

	@property
	def expand(self):
		"""Resources in town centers."""
		return self._investments[2]

	@expand.setter
	def expand(self, value):
		self._investments[2] = value

	@property
	def production(self):
		"""Resources in production potential."""
		return self._investments[3]

	@production.setter
	def production(self, value):
		self._investments[3] = value
