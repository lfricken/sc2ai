import os
import pickle
from typing import Iterator

from utils.Directories import Directories
from utils.ProgressBar import *
from utils.TrainingData import TrainingData


class FileEnumerable:
	"""Loops over directories easier."""

	@staticmethod
	def get_file_count(directory: str, extension: str) -> int:
		num_files = 0
		for (path, filename) in FileEnumerable.get_files_enumerable(directory):
			if filename.endswith(extension):
				num_files += 1
		return num_files

	@staticmethod
	def get_analysis_enumerable() -> Iterator[TrainingData]:
		"""Loops over analysis data and returns each TrainingData."""
		extension = ".pkl"
		file_count = FileEnumerable.get_file_count(Directories.analysis(), extension)

		print("{} {} files in directory".format(file_count, extension))

		for filename in os.listdir(Directories.analysis()):
			if filename.endswith(extension):
				with open(os.path.join(Directories.analysis(), filename), "rb") as infile:
					analysis_data: TrainingData = pickle.load(infile)
					yield analysis_data

	@staticmethod
	def get_replays_dirs_enumerable(show_progress: bool = True) -> (str, str):
		"""
		Loops over replay files and the expected output analysis."""

		extension = ".SC2Replay"
		file_count = FileEnumerable.get_file_count(Directories.replays(), extension)

		print("{} {} files in directory".format(file_count, extension))

		if show_progress:
			start_progress("Analyzing Replays")
		num_files_processed = 0

		for (path, filename) in FileEnumerable.get_files_enumerable(Directories.replays()):
			if filename.endswith(extension):
				replay_file = os.path.join(path, filename)
				replay_analysis_file = os.path.join(Directories.analysis(), filename + ".pkl")
				yield (replay_file, replay_analysis_file)
				num_files_processed += 1
				if show_progress:
					progress(num_files_processed / file_count)

		if show_progress:
			end_progress()
			print("Done!")

	@staticmethod
	def get_files_enumerable(root: str) -> (str, str):
		"""Full path and file name"""
		for path, _, files in os.walk(root):
			for name in files:
				yield (path, name)
