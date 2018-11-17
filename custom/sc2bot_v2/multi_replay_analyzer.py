# This script should:
# 1. take in a directory as an argument
# 2. analyze every replay in it
# 3. write the data to a file

import os
import pickle

import sc2reader
from sc2reader.resources import Replay

from utils.PlayerData import PlayerData
from utils.TrainingData import TrainingData

directory = "C:\\dev\\ai\\sc2\\sc2ai\\replays"


def process_replay(full_file_path) -> TrainingData:
	replay: Replay = sc2reader.load_replay(full_file_path, load_level=4)
	player_1_data = PlayerData(replay.players[0], replay.frames)
	player_2_data = PlayerData(replay.players[1], replay.frames)

	return TrainingData(player_1_data, player_2_data)


for filename in os.listdir(directory):
	if filename.endswith(".SC2Replay"):
		training_session = process_replay(os.path.join(directory, filename))
		output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "analysis")
		with open(os.path.join(output_dir, filename + ".pkl"), "wb") as outfile:
			pickle.dump(training_session, outfile, pickle.HIGHEST_PROTOCOL)
