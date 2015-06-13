#!/usr/bin/python

import sys
import math
import mmh3
import random
import string
import binascii

class BitArray(object):
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

class BloomFilter(object):
	def __init__(self, n, k, seedLimit = 1000):
		self.n = n
		self.k = k

		self.array = BitArray(n)
		self.expansionFactor = self.array.expansionFactor(128) # _hash returns 128 bits

		# Create the k hash functions
		self.ivs = []
		for i in range(k):
			val = random.randint(0, seedLimit)
			while val in self.ivs:
				val = random.randint(0, seedLimit)
			self.ivs.append(val)

	def _hash(self, k, val):
		''' Return 128-bits as bytes
		'''
		bits = "" 
		for e in range(self.expansionFactor):
			digest = mmh3.hash_bytes(str(val) + str(e), self.ivs[k])
			bits = bits + digest
		return bits

	def _digestToBitIndices(self, digest):
		indices = []

		bitString = int(binascii.b2a_hex(digest), 16)

		bitRange = len(digest) * 8 # digest is a byte-string
		for index in range(bitRange):
			if ((1 << index) & (bitString) > 0):
				indices.append(index)

		return indices
		
	def insert(self, val):
		for k in range(self.k):
			bits = self._hash(k, val)
			bitIndices = self._digestToBitIndices(bits)
			for b in bitIndices:
				self.array.setBit(b)

	def contains(self, element):
		for k in range(self.k):
			bits = self._hash(k, str(element))
			bitIndices = self._digestToBitIndices(bits)
			for b in bitIndices:
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

def playWithFilter(n, k = 2):
	bf = BloomFilter(n, 2)
	v1 = "rawrawrawrawrawrawrawrawr"
	bf.insert(v1)
	print bf.contains("hello?")
	print bf.contains(v1)

def findCollision(n, k = 2):
	bf = BloomFilter(n, 2)
	test = "Hello world"
	bf.insert(test)
	print bf.contains(test)
	found = False
	val = ""
	while not found:
		val = (''.join(random.choice(string.ascii_uppercase) for i in range(128)))
		if bf.contains(val):
			print "Found collision", test, val
			found = True
	return test, val

def main(args):
	n = int(sys.argv[1])
	k = int(sys.argv[2])

	# stupid tests...
	playWithArray(n)
	playWithFilter(n, k)
	findCollision(n, k)

	return

if __name__ == "__main__":
	main(sys.argv)
