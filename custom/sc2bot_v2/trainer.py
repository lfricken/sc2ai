# trains a neural network with data from the analysis folder
# you need to generate the analysis data first

import os
import pickle

from utils.Directories import Directories
from utils.TrainingData import TrainingData


def train_with_analysis(data: TrainingData):
	return


for filename in os.listdir(Directories.analysis()):
	if filename.endswith(".pkl"):
		with open(os.path.join(Directories.analysis(), filename), "rb") as infile:
			analysis_data = pickle.load(infile)
			train_with_analysis(analysis_data)
