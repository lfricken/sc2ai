from typing import Iterator

import os

from sc2ai.utils.FileEnumerable import FileEnumerable
from sc2ai.utils.TrainingData import *
from sc2ai.utils.Investments import *


class TrainingValues(Investments):
    """Useful values for training networks."""

    @staticmethod
    def get_training_enumerable() -> Iterator[TrainingData]:
        """Allows you to loop over training data files."""
        for _ in FileEnumerable.get_analysis_enumerable():
            yield _

    @staticmethod
    def argmax(x: [int]) -> int:
        """Returns index of largest value."""
        return max(range(len(x)), key=x.__getitem__)

    @staticmethod
    def num_zt_units() -> int:
        """Returns number of zerg + terran unit types"""
        return ZergInvestments.num_values() + TerranInvestments.num_values()

    @staticmethod
    def num_coreinvest_inputs() -> int:
        """Returns size of input if you want to pass both players core investments."""
        return CoreInvestments.num_values() * 2  # x2 because enemy values

    @staticmethod
    def num_coreinvest_outputs() -> int:
        """Returns size of input if you want to produce core investments."""
        return CoreInvestments.num_values()

    @staticmethod
    def get_save_directory(num_inputs: int, num_hidden: int, num_outputs: int) -> str:
        """Generates the local save path+file for a given network."""
        return os.path.dirname(os.path.abspath(__file__)) + "/../brains/{}_{}_{}_brain.ckpt".format(num_inputs, num_hidden, num_outputs)

    @staticmethod
    def get_tensorboard_directory() -> str:
        """Generates the local save path+file for a given network."""
        return os.path.dirname(os.path.abspath(__file__)) + "\\..\\tensorboard"
