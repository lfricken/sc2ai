import os


class Directories:
	"""Relevant directories."""

	@staticmethod
	def project() -> str:
		"""Folder that contains this project."""
		return os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")

	@staticmethod
	def analysis() -> str:
		"""Folder that contains replay analysis."""
		return os.path.join(Directories.project(), "analysis")

	@staticmethod
	def root() -> str:
		"""Folder that contains this project's folder."""
		custom_dir = os.path.join(Directories.project(), "..")
		return os.path.join(custom_dir, "..")

	@staticmethod
	def replays() -> str:
		"""Folder that contains this project's folder."""
		return os.path.join(Directories.root(), "replays")
