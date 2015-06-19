import math

class BitArray(object):
	''' Simple implementation of a bitarray or bitmap.
	'''
	def __init__(self, length):
		self.indexSize = 32
		self.length = int(math.ceil(length / self.indexSize))
		self.array = [0,] * self.length

	def __str__(self):
		return "Array["+ str(self.length * self.indexSize) + "]: " + str(self.array)

	def expansionFactor(self, base):
		return (self.length * self.indexSize) / base

	def getBit(self, index):
		offset = index % self.indexSize
		index = index / self.indexSize
		val = 1 if int((self.array[index] & (1 << offset))) > 0 else  0
		return val

	def isBitSet(self, bit):
		return (self.getBit(bit) == 1)

	def setBit(self, index):
		offset = index % self.indexSize
		index = index / self.indexSize
		self.array[index] = self.array[index] | (1 << offset)
