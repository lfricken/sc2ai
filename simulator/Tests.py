from Simulator import *

import unittest


class SimulatorTest(unittest.TestCase):
	def test_CloserPositions0(self):
		sim = Simulator()
		pos: [VectorInt] = sim.get_closer_positions(VectorInt(0, 0), VectorInt(0, 1), 2)

		self.assertTrue(pos[0].x == 1)
		self.assertTrue(pos[1].x == 0)
		self.assertTrue(pos[2].x == -1)

		self.assertTrue(pos[0].y == 0)
		self.assertTrue(pos[1].y == 0)
		self.assertTrue(pos[2].y == 0)

	def test_CloserPositions45(self):
		sim = Simulator()
		pos: [VectorInt] = sim.get_closer_positions(VectorInt(0, 0), VectorInt(1, 1))

		self.assertTrue(pos[0].x == 1)
		self.assertTrue(pos[1].x == 0)
		self.assertTrue(pos[2].x == 0)

		self.assertTrue(pos[0].y == 0)
		self.assertTrue(pos[1].y == 0)
		self.assertTrue(pos[2].y == 1)

	def test_CloserPositions90(self):
		sim = Simulator()
		pos: [VectorInt] = sim.get_closer_positions(VectorInt(0, 0), VectorInt(1, 0))

		self.assertTrue(pos[0].x == 0)
		self.assertTrue(pos[1].x == 0)
		self.assertTrue(pos[2].x == 0)

		self.assertTrue(pos[0].y == -1)
		self.assertTrue(pos[1].y == 0)
		self.assertTrue(pos[2].y == 1)

	def test_AddUnitAddsBoth(self):
		sim = Simulator()
		position = VectorInt(0, 0)
		expected_number = 1
		team: Team = Team.Red

		sim.try_add_unit("Marine", position, team)
		cell_units: [Unit] = sim.get_cell(position).get_units

		self.assertEqual(len(sim.units[team]), expected_number)
		self.assertEqual(len(cell_units[team]), expected_number)

	def test_InRange(self):
		sim = Simulator()
		position = VectorInt(0, 0)

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

		sim.try_add_unit("Marine", VectorInt(0, 0), Team.Blue)
		sim.try_add_unit("Marine", VectorInt(7, 0), Team.Red)

		sim.apply_attacks(1.0)
		health = sim.units[Team.Blue][0].health
		self.assertAlmostEqual(health, 55.0)

	def test_NoOverkill(self):
		sim = Simulator()

		pos = VectorInt(0, 0)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		pos = VectorInt(0, 1)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		pos = VectorInt(0, 2)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)
		sim.try_add_unit("Marine", pos, Team.Blue)

		pos = VectorInt(1, 1)
		sim.try_add_unit("Marine", pos, Team.Red)
		sim.try_add_unit("Marine", pos, Team.Red)

		sim.apply_attacks(1.0)

		self.assertTrue(not sim.units[Team.Red][0].alive)
		self.assertTrue(not sim.units[Team.Red][1].alive)


if __name__ == '__main__':
	unittest.main()
