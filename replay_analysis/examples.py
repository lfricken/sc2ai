# Don't modify this file, this is meant as a simple example.
import sc2reader


def replay_directory():
	return "replays/"


def test_hots_hatchfun():
	return sc2reader.load_replay(replay_directory() + "Example.SC2Replay", load_level=4)


replay = test_hots_hatchfun()

unit_value = 0
current_increment = 0
game_increments = replay.real_length.seconds * 2 * 11

for player in replay.players:

	while current_increment < game_increments:

		for unit in player.units:
			if unit.minerals > 0 and unit.is_army:
				if unit.died_at is not None and unit.finished_at is not None:
					if unit.finished_at <= current_increment < unit.died_at:
						unit_value += unit.minerals + unit.vespene
		print(unit_value)
		unit_value = 0

		current_increment += 100

	break
