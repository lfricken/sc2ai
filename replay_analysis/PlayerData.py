class PlayerData:
	"""Contains data over time about this player."""

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
