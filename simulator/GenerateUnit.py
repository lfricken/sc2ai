from Map import *


def generate_type(unit_name: str) -> Unit:
	unit = Unit()

	if unit_name == "Marine":
		unit = Unit()
		unit.dps = 9.8
		unit.size = 0.8
		unit.max_range = 5.0
		unit.speed = 3.15
		unit.health = 55

	return unit
