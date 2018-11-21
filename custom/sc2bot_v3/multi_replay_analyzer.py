# This script should:
# 1. take in a directory as an argument
# 2. analyze every replay in it
# 3. write the data to a file

import pickle

import sc2reader
from sc2reader.resources import Replay

from utils.FileEnumerable import FileEnumerable
from utils.PlayerData import PlayerData
from utils.TrainingData import TrainingData
from mpyq import MPQArchive


def process_replay(full_file_path):
	"""Turns the replay into analyzed data."""
	archive = MPQArchive(full_file_path)
	files = archive.extract()
	replay: Replay = sc2reader.load_replay(full_file_path, load_level=4)

	p1 = replay.players[0]
	p2 = replay.players[1]
	t_won = (p1.play_race == "Terran" and p1.result == "Win") or (p2.play_race == "Terran" and p2.result == "Win")
	p_won = (p1.play_race == "Protoss" and p1.result == "Win") or (p2.play_race == "Protoss" and p2.result == "Win")

	if t_won or p_won:
		player_1_data = PlayerData(replay.players[0], replay.frames)
		player_2_data = PlayerData(replay.players[1], replay.frames)
		return TrainingData(player_1_data, player_2_data)
	else:
		return None


for (replay_file, replay_analysis_file) in FileEnumerable.get_replays_dirs_enumerable():
	training_data = process_replay(replay_file)
	if training_data is not None:
		with open(replay_analysis_file, "wb") as outfile:
			pickle.dump(training_data, outfile, pickle.HIGHEST_PROTOCOL)
