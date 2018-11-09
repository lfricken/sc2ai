import sc2reader


def replay_directory():
	return "../replays/"


def test_hots_hatchfun():
	return sc2reader.load_replay(replay_directory() + "Example.SC2Replay", load_level=4)



replay = test_hots_hatchfun()

replay.work()
