import numpy as np
from keras.api.utils import Sequence

from PIL import Image 

class ThumbnailDataGenerator(Sequence):

	def __init__(self, filedir : str, list_IDs : list[str], labels : dict[str, float], rescale : float=255.0, filetype : str="jpg", batch_size : int=32, dim : tuple[int, int]=(90, 120), shuffle=True):
		'''
		Data Generator Initialization Function 
		'''
		self.filedir = filedir
		self.filetype = filetype
		self.dim = dim
		self.rescale = rescale
		self.batch_size = batch_size
		self.labels = labels
		self.list_IDs = list_IDs
		self.shuffle = shuffle
		self.on_epoch_end()

	def on_epoch_end(self):
		'''
		Updates indexes after each epoch
		'''
		self.indexes = np.arange(len(self.list_IDs))

		# Randomize if Shuffle
		if self.shuffle:
			np.random.shuffle(self.indexes)

	def __data_generation(self, list_IDs_temp):
		'''
		Generates data containing batch_size samples
		'''
		# Initialization
		X = np.empty((self.batch_size, *self.dim, 3))
		y = np.empty((self.batch_size), dtype=float)

		# Generate data
		for i, ID in enumerate(list_IDs_temp):
			# Store sample
			X[i,] = Image.open(f'{self.filedir}/{ID}.{self.filetype}')

			# Store class
			y[i] = self.labels[ID]

		# Rescale
		X /= self.rescale

		return X, y
	
	def __len__(self):
		'''
		Denotes the number of batches per epoch
		'''
		return int(np.floor(len(self.list_IDs) / self.batch_size))
	
	def __getitem__(self, index):
		'''
		Generate one batch of data
		'''
		# Generate indexes of the batch
		indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

		# Find list of IDs
		list_IDs_temp = [self.list_IDs[k] for k in indexes]

		# Generate data
		return self.__data_generation(list_IDs_temp)