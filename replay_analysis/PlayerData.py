class PlayerData:
	"""
	Contains data about this player over the course of the game.
	Used for a neural network to train on successful investment strategies.
	"""

	army_value = []
	"""Total resources invested in research at a given time."""
	research = []
	"""Total resources invested in research at a given time."""
	technology = []
	"""Total resources invested in the tech tree at a given time."""
	expands = []
	"""How many expands do we have at a given time."""
	income_per_minute = []
	"""(minerals,vespene) income per minute at a given time."""

	def __init__(self, player):
		return
