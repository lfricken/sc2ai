# This script should:
# 1. take in a directory as an argument
# 2. analyze every replay in it
# 3. write the data to a file

import pickle
import os

import sc2reader
import os
from sc2reader.resources import Replay

from sc2ai.utils.FileEnumerable import FileEnumerable
from sc2ai.utils.PlayerData import *
from sc2ai.utils.TrainingData import TrainingData
from sc2ai.utils.Directories import Directories


def race_win_lose(race_win, race_lose, p1, p2) -> bool:
    return ((p1.play_race == race_win and p1.result == "Win") or (p2.play_race == race_win and p2.result == "Win")) and \
           ((p1.play_race == race_lose and p1.result == "Lose") or (p2.play_race == race_lose and p2.result == "Lose"))


def process_replay(replay: Replay) -> TrainingData:
    """Turns the replay into analyzed data."""

    if replay.players[0].play_race == "Zerg" and replay.players[1].play_race == "Terran":
        zerg = 0
        other = 1
    elif replay.players[0].play_race == "Terran" and replay.players[1].play_race == "Zerg":
        zerg = 1
        other = 0
    else:
        return None
    
    # TODO: there was some issue here occasionally
    try:
        vals = type('', (), {})()  # lets you assign any variable
        vals.player = replay.players[zerg]
        vals.total_frames = replay.frames
        # TODO: just have PlayerData infer race
        player_1_data = ZergData(vals)

        vals = type('', (), {})()  # lets you assign any variable
        vals.player = replay.players[other]
        vals.total_frames = replay.frames
        player_2_data = TerranData(vals)

        data = TrainingData(player_1_data, player_2_data)

        return data
    except:
        return None


for (replay_file, replay_analysis_file) in FileEnumerable.get_replays_dirs_enumerable():

    # if already parsed the replay, continue
    if os.path.isfile(replay_analysis_file):
        print("File skipped because it already exists: {}".format(replay_analysis_file))
        continue
    
    # start = time.time()
    loaded_replay: Replay = sc2reader.load_replay(replay_file, load_level=3)
    # end = time.time()
    # print("Reading took " + str(end - start))

    # start = time.time()
    training_data = process_replay(loaded_replay)
    # end = time.time()
    # print("Analyzing took " + str(end - start))

    # start = time.time()
    if training_data:
        if not os.path.exists(Directories.analysis()):
            os.makedirs(Directories.analysis())
        with open(replay_analysis_file, "wb") as outfile:
            pickle.dump(training_data, outfile, pickle.HIGHEST_PROTOCOL)
# end = time.time()
# print("Saving took " + str(end - start))
