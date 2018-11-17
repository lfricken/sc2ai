# This script should:
# 1. take in a directory as an argument
# 2. analyze every replay in it
# 3. write the data to a file

import pickle

import sc2reader
from sc2reader.resources import Replay

from utils.Directories import *
from utils.PlayerData import PlayerData
from utils.ProgressBar import *
from utils.TrainingData import TrainingData


def process_replay(full_file_path) -> TrainingData:
	replay: Replay = sc2reader.load_replay(full_file_path, load_level=4)
	player_1_data = PlayerData(replay.players[0], replay.frames)
	player_2_data = PlayerData(replay.players[1], replay.frames)

	return TrainingData(player_1_data, player_2_data)


num_replays = 0
for filename in os.listdir(Directories.replays()):
	if filename.endswith(".SC2Replay"):
		num_replays += 1

print("%s files in directory" % num_replays)
start_progress("Analyzing Replays")

num_files_processed = 0
for filename in os.listdir(Directories.replays()):
	if filename.endswith(".SC2Replay"):
		training_session = process_replay(os.path.join(Directories.replays(), filename))
		with open(os.path.join(Directories.analysis(), filename + ".pkl"), "wb") as outfile:
			pickle.dump(training_session, outfile, pickle.HIGHEST_PROTOCOL)
			num_files_processed += 1
			progress(num_files_processed / num_replays)

end_progress()
print("Done!")
