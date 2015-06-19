import math
from threading import Thread, Lock

class BitArray(object):
	''' Simple implementation of a bitarray or bitmap.
	'''
	def __init__(self, length):
		self.indexSize = 32
		self.length = int(math.ceil(length / self.indexSize))
		self.array = [0,] * self.length

	def __str__(self):
		return "Array["+ str(self.length * self.indexSize) + "]: " + str(self.array)

	def size(self):
		return self.length * self.indexSize

	def expansionFactor(self, base):
		return (self.length * self.indexSize) / base

	def getValue(self, index):
		offset = index % self.indexSize
		index = index / self.indexSize
		val = 1 if int((self.array[index] & (1 << offset))) > 0 else  0
		return val

	def isEmpty(self, bit):
		return (self.getValue(bit) == 0)

	def addAt(self, index):
		offset = index % self.indexSize
		index = index / self.indexSize
		self.array[index] = self.array[index] | (1 << offset)

class CoutingArray(object):
	''' Simple implementation of a bitarray or bitmap.
	'''
	def __init__(self, length):
		''' Each entry is a counter, not a single bit.
		'''
		self.array = [0,] * self.length
		self.lock = Lock()

	def __str__(self):
		return "CountingArray["+ str(self.length) + "]: " + str(self.array)

	def size(self):
		return self.length

	def expansionFactor(self, base):
		return self.length / base

	def getValue(self, index):
		mutex.acquire()
		value = 0
		try:
			value = self.array[index]
		finally:
			mutex.release()
		return value

	def isEmpty(self, bit):
		return (self.getCount(bit) == 0)

	def addAt(self, index):
		mutex.acquire()
		try:
			self.array[index] += 1
		finally:
			mutex.release()

	def removeAt(self, index):
		mutex.acquire()
		try:
			if self.array[index] > 0:
				self.array[index] += 1
			else:
				pass # this is not an exception
		finally:
			mutex.release()
