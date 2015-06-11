#!/usr/bin/python

import sys
import math
import mmh3

class BitArray(object):
	def __init__(self, length):
		self.length = int(math.ceil(length / 8))
		self.array = (0,) * self.length

	def __str__(self):
		return "Array["+ str(self.length * 8) + "]: " + str(self.array)

	def get(self, index):
		index = index / 8
		return self.array[index]

	def set(self, index):
		pass

class BloomFilter(object):
	def __init__(self):
		pass

def main(args):
	n = int(sys.argv[1])
	array = BitArray(n)
	print array
	pass

if __name__ == "__main__":
	main(sys.argv)

