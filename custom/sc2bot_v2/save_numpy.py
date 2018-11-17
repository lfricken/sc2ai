import pickle

import numpy as np

array = list()
array.append(np.array([1, 2, 3, 4, 5]))
array.append(np.array([1, 2, 3, 4, 5]))

with open('mat.pkl', 'wb') as outfile:
	pickle.dump(array, outfile, pickle.HIGHEST_PROTOCOL)

with open('mat.pkl', 'rb') as infile:
	result = pickle.load(infile)

print("hi")
