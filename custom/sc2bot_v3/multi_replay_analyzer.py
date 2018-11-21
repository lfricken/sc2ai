# This script should:
# 1. take in a directory as an argument
# 2. analyze every replay in it
# 3. write the data to a file

import pickle

import sc2reader
from sc2reader.resources import Replay

from utils.FileEnumerable import FileEnumerable
from utils.PlayerData import *
from utils.TrainingData import TrainingData


def race_win_lose(race_win, race_lose, p1, p2) -> bool:
	return ((p1.play_race == race_win and p1.result == "Win") or (p2.play_race == race_win and p2.result == "Win")) and \
	       ((p1.play_race == race_lose and p1.result == "Lose") or (p2.play_race == race_lose and p2.result == "Lose"))


def process_replay(full_file_path):
	"""Turns the replay into analyzed data."""
	replay: Replay = sc2reader.load_replay(full_file_path, load_level=4)

	if replay.players[0].play_race == "Zerg":
		zerg = 0
		other = 1
	else:
		zerg = 1
		other = 0

	vals = type('', (), {})()
	vals.player = replay.players[zerg]
	vals.total_frames = replay.frames
	player_1_data = ZergData(vals)

	vals = type('', (), {})()
	vals.player = replay.players[other]
	vals.total_frames = replay.frames
	player_2_data = TerranData(vals)

	# have Zerg (us) be first
	if replay.players[0].play_race == "Zerg":
		return TrainingData(player_1_data, player_2_data)
	else:
		return TrainingData(player_2_data, player_1_data)


for (replay_file, replay_analysis_file) in FileEnumerable.get_replays_dirs_enumerable():
	training_data = process_replay(replay_file)
	if training_data is not None:
		with open(replay_analysis_file, "wb") as outfile:
			pickle.dump(training_data, outfile, pickle.HIGHEST_PROTOCOL)
