# This script should:
# 1. take in a directory as an argument
# 2. analyze every replay in it
# 3. write the data to a file

import sc2reader
from sc2reader.resources import Replay

from PlayerData import PlayerData


def process_replay(full_file_path):
	replay: Replay = sc2reader.load_replay(full_file_path, load_level=4)
	data = PlayerData(replay.players[0], replay.frames)
	print("done")


process_replay("replays/Example.SC2Replay")

# directory = "C:\\dev\\ai\sc2\\replays"
# for filename in os.listdir(directory):
#	process_replay(os.path.join(directory, filename))
