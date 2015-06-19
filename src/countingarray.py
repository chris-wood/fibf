import math

class CoutingArray(object):
	''' Simple implementation of a bitarray or bitmap.
	'''
	def __init__(self, length):
        ''' Each entry is a counter, not a single bit.
        '''
		self.array = [0,] * self.length

	def __str__(self):
		return "CountingArray["+ str(self.length) + "]: " + str(self.array)

	def expansionFactor(self, base):
		return self.length / base

	def getValue(self, index):
        return self.array[index]

	def isEmpty(self, bit):
		return (self.getCount(bit) == 0)

	def addAt(self, index):
        self.array[index] += 1

    def removeAt(self, index):
		if self.array[index] > 0:
        	self.array[index] -= 1
		else:
			pass # this not an exception
