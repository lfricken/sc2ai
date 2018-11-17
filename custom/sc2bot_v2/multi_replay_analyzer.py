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


def process_replay(full_file_path) -> TrainingData:
	"""Turns the replay into analyzed data."""

	replay: Replay = sc2reader.load_replay(full_file_path, load_level=4)
	player_1_data = PlayerData(replay.players[0], replay.frames)
	player_2_data = PlayerData(replay.players[1], replay.frames)

	return TrainingData(player_1_data, player_2_data)


for (replay_file, replay_analysis_file) in FileEnumerable.get_replays_dirs_enumerable():
	training_data = process_replay(replay_file)
	with open(replay_analysis_file, "wb") as outfile:
		pickle.dump(training_data, outfile, pickle.HIGHEST_PROTOCOL)
