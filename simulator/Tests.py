from Simulator import *

import unittest


class SimulatorTest(unittest.TestCase):
	def test_AddUnitAddsBoth(self):
		sim = Simulator()
		position = (0, 0)
		expected_number = 1
		team: Team = Team.Red

		sim.try_add_unit("Marine", position, team)
		cell_units: [Unit] = sim.get_cell(position).get_units

		self.assertEqual(len(sim.units[team]), expected_number)
		self.assertEqual(len(cell_units[team]), expected_number)

	def test_InRange(self):
		sim = Simulator()
		position = (0, 0)

		sim.try_add_unit("Marine", position, Team.Blue)
		sim.try_add_unit("Marine", position, Team.Red)

		sim.apply_attacks(1.0)
		health = sim.units[Team.Blue][0].health
		self.assertAlmostEqual(health, 55.0 - 9.8 * 1)

		health = sim.units[Team.Red][0].health
		self.assertAlmostEqual(health, 55.0 - 9.8 * 1)

		sim.apply_attacks(1.0)
		health = sim.units[Team.Blue][0].health
		self.assertAlmostEqual(health, 55.0 - 9.8 * 2)

	def test_OutOfRange(self):
		sim = Simulator()

		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (7, 0), Team.Red)

		sim.apply_attacks(1.0)
		health = sim.units[Team.Blue][0].health
		self.assertAlmostEqual(health, 55.0)

	def test_NoOverkill(self):
		sim = Simulator()

		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (0, 1), Team.Blue)
		sim.try_add_unit("Marine", (0, 1), Team.Blue)
		sim.try_add_unit("Marine", (0, 1), Team.Blue)
		sim.try_add_unit("Marine", (0, 1), Team.Blue)
		sim.try_add_unit("Marine", (0, 1), Team.Blue)
		sim.try_add_unit("Marine", (0, 2), Team.Blue)
		sim.try_add_unit("Marine", (0, 2), Team.Blue)
		sim.try_add_unit("Marine", (0, 2), Team.Blue)
		sim.try_add_unit("Marine", (0, 2), Team.Blue)
		sim.try_add_unit("Marine", (0, 2), Team.Blue)

		sim.try_add_unit("Marine", (1, 1), Team.Red)
		sim.try_add_unit("Marine", (1, 1), Team.Red)

		sim.apply_attacks(1.0)

		self.assertTrue(not sim.units[Team.Red][0].alive)
		self.assertTrue(not sim.units[Team.Red][1].alive)


if __name__ == '__main__':
	unittest.main()
