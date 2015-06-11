#!/usr/bin/python

import sys
import math
import mmh3
import random

class BitArray(object):
	def __init__(self, length):
		self.indexSize = 32
		self.length = int(math.ceil(length / self.indexSize))
		self.array = [0,] * self.length

	def __str__(self):
		return "Array["+ str(self.length * self.indexSize) + "]: " + str(self.array)

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

class BloomFilter(object):
	def __init__(self, n, k, seedLimit = 1000):
		self.n = n
		self.k = k

		self.array = BitArray(n)

		# Create the k hash functions
		self.ivs = []
		for i in range(k):
			val = random.randint(0, seedLimit)
			while val in self.ivs:
				val = random.randint(0, seedLimit)
			self.ivs.append(val)

	def _hash(self, k, val):
		return mmh3.hash(val, self.ivs[k])

	def _digestToBitIndices(self, digest):
		pass
		
	def insert(self, val):
		for k in range(self.k):
			digest = self._hash(k, val)
			bits = self._digestToBitIndices(digest)

			for b in bits:
				self.array.setBit(b)

	def contains(self, element):
		for k in range(self.k):
			digest = self._hash(k, val)
			bits = self._digestToBitIndices(digest)
			for b in bits:
				if not self.array.isBitSet(b):
					return False
		return True

def playWithArray(n):
	array = BitArray(n)
	print array
	array.setBit(4)
	print array
	print array.getBit(4)
	print array.getBit(5)

def main(args):
	n = int(sys.argv[1])
	playWithArray(n)

	
	
	# return OK
	pass

if __name__ == "__main__":
	main(sys.argv)

