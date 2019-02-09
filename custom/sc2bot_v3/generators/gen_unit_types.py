# This script should:
# 1. take in a directory as an argument
# 2. analyze every replay in it
# 3. write the data to a file

import os

import sc2reader
from sc2reader.data import Unit
from sc2reader.resources import Replay

from sc2ai.utils.FileEnumerable import FileEnumerable
from sc2ai.utils.Investments import in_exceptions, fix_name

dir_path = os.path.dirname(os.path.realpath(__file__))
terran = dict()
zerg = dict()
protoss = dict()


def add_unit(race, unit: Unit):
	if race == "Terran":
		dic = terran
	elif race == "Zerg":
		dic = zerg
	else:
		dic = protoss
	if unit.is_worker or unit.is_building or unit.is_army:
		for t, v in unit.type_history.items():
			if in_exceptions(v.name):
				v.name = fix_name(v.name)
			if v.name != "":
				dic.update({v.name.upper(): 0})


def process_replay(full_file_path):
	"""Turns the replay into analyzed data."""
	replay: Replay = sc2reader.load_replay(full_file_path, load_level=4)

	for player in replay.players:
		for unit in player.units:
			add_unit(player.play_race, unit)


def to_file(file_name: str, data: dict):
	if len(data) == 0:
		return

	f = open(os.path.join(dir_path, file_name + "_unit_types.txt"), "w+")
	print("\n\n{}\n".format(file_name))
	for key, value in data.items():
		line = key
		print(line)
		f.write(line + "\n")
	f.close()


i = 0
for (replay_file, replay_analysis_file) in FileEnumerable.get_replays_dirs_enumerable(show_progress=False):
	i += 1
	process_replay(replay_file)
	if i > 100:
		break

to_file("terran", terran)
to_file("zerg", zerg)
to_file("protoss", protoss)
