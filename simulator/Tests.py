from Simulator import *

import unittest


class SimulatorTest(unittest.TestCase):
	def test_MapWorks(self):
		sim = Simulator()

		# terrain lets us set its values
		pos = (1, 1)
		sim.map.set_type(pos, TerrainFlags.raised)
		self.assertTrue(sim.map.is_type(pos, TerrainFlags.raised))

		# most terrain is empty
		pos = (0, 0)
		self.assertFalse(sim.map.is_type(pos, TerrainFlags.raised))
		self.assertFalse(sim.map.is_type(pos, TerrainFlags.void))
		self.assertFalse(sim.map.is_type(pos, TerrainFlags.cliff))
		self.assertFalse(sim.map.is_type(pos, TerrainFlags.filled))

		# filling
		pos = (0, 0)
		self.assertFalse(sim.map.set_type(pos, TerrainFlags.filled))
		sim.map.set_type(pos, TerrainFlags.filled)
		self.assertTrue(sim.map.set_type(pos, TerrainFlags.filled))

		# unfilling
		pos = (0, 0)
		sim.map.set_type(pos, TerrainFlags.filled)
		self.assertTrue(sim.map.set_type(pos, TerrainFlags.filled))
		sim.map.unfill(pos)
		self.assertFalse(sim.map.set_type(pos, TerrainFlags.filled))

	def test_AddUnitAddsBoth(self):
		sim = Simulator()
		position = (0, 0)
		expected_number = 1
		team: Team = Team.Red

		sim.try_add_unit("Marine", position, team)

		self.assertEqual(len(sim.units[team]), expected_number)

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

	def test_NoOverfill(self):
		sim = Simulator()

		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		sim.try_add_unit("Marine", (0, 0), Team.Blue)
		five_added = sim.try_add_unit("Marine", (0, 0), Team.Blue)
		six_added = sim.try_add_unit("Marine", (0, 0), Team.Blue)
		six_enemy_added = sim.try_add_unit("Marine", (0, 0), Team.Red)

		self.assertTrue(five_added)
		self.assertTrue(not six_added)
		self.assertTrue(not six_enemy_added)


if __name__ == '__main__':
	unittest.main()
