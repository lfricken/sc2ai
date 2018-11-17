import os
import pickle
from typing import Generator

from utils.Directories import Directories
from utils.ProgressBar import *
from utils.TrainingData import TrainingData


class FileEnumerable:
	"""Loops over directories easier."""

	@staticmethod
	def get_analysis_enumerable() -> Generator[TrainingData]:
		"""Loops over analysis data and returns each TrainingData."""

		num_files = 0
		for filename in os.listdir(Directories.replays()):
			if filename.endswith(".SC2Replay"):
				num_files += 1

		print("%s files in directory" % num_files)
		start_progress("Training with data")
		num_files_processed = 0

		for filename in os.listdir(Directories.analysis()):
			if filename.endswith(".pkl"):
				with open(os.path.join(Directories.analysis(), filename), "rb") as infile:
					analysis_data: TrainingData = pickle.load(infile)
					yield analysis_data
					num_files_processed += 1
					progress(num_files_processed / num_files)

		end_progress()
		print("Done!")

	@staticmethod
	def get_replays_dirs_enumerable() -> Generator[(str, str)]:
		"""Loops over replay files and the expected output analysis."""

		num_replays = 0
		for filename in os.listdir(Directories.replays()):
			if filename.endswith(".SC2Replay"):
				num_replays += 1

		print("%s files in directory" % num_replays)
		start_progress("Analyzing Replays")
		num_files_processed = 0

		for filename in os.listdir(Directories.replays()):
			if filename.endswith(".SC2Replay"):
				replay_file = os.path.join(Directories.replays(), filename)
				replay_analysis_file = os.path.join(Directories.analysis(), filename + ".pkl")
				yield (replay_file, replay_analysis_file)
				num_files_processed += 1
				progress(num_files_processed / num_replays)

		end_progress()
		print("Done!")
