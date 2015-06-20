#!/usr/bin/python

import sys
import math
import mmh3
import random
import string
import binascii
import hashlib
import threading
import time
from Crypto.Cipher import AES
from bitarray import *

class BloomFilter(object):
    def __init__(self, array, k, seedLimit = 1000):
        self.k = k

        self.array = array
        self.expansionFactor = self.array.expansionFactor(128) # _digest returns 128 bits

        # Create the k hash functions
        self.ivs = []
        for i in range(k):
            val = random.randint(0, seedLimit)
            while val in self.ivs:
                val = random.randint(0, seedLimit)
            self.ivs.append(val)

    def _randomString(self, length):
        return (''.join(random.choice(string.ascii_uppercase) for i in range(length)))

    def _hashDigest(self, key, val, iv):
        return mmh3.hash_bytes(str(val) + str(iv), key)

    def _digest(self, k, val):
        ''' Return 128-bits as bytes
        '''
        bits = ""
        for e in range(self.expansionFactor):
            digest = self._hashDigest(self.ivs[k], str(val), str(e))
            bits = bits + digest
        return bits

    def _digestToBitIndices(self, digest):
        indices = []

        bitString = int(binascii.b2a_hex(digest), 16)
        bitRange = len(digest) * 8 # digest is a byte string

        for index in range(bitRange):
            if ((1 << index) & (bitString) > 0):
                indices.append(index)

        return indices

    def insert(self, val):
        for k in range(self.k):
            bits = self._digest(k, val)
            bitIndices = self._digestToBitIndices(bits)
            for b in bitIndices:
                self.array.addAt(b)

    def contains(self, element):
        for k in range(self.k):
            bits = self._digest(k, str(element))
            bitIndices = self._digestToBitIndices(bits)
            for b in bitIndices:
                if self.array.isEmpty(b):
                    return False
        return True

class Decayer(threading.Thread):
    def __init__(self, array, updateInterval):
        threading.Thread.__init__(self)
        self.array = array
        self.updateInterval = updateInterval

    def run(self):
        while True:
            for index in range(self.array.size()):
                self.array.removeAt(index)
            time.sleep(self.updateInterval)
            print self.array

class DecayingBloomFilter(BloomFilter):
    def __init__(self, n, k, updateInterval, seedLimit = 1000):
        self.array = CountingArray(n)
        self.updateInterval = updateInterval
        BloomFilter.__init__(self, self.array, k, seedLimit)
        decayer = Decayer(self.array, self.updateInterval)
        decayer.start()

class CountingBloomFilter(BloomFilter):
    def __init__(self, n, k, seedLimit = 1000):
        array = CountingArray(n)
        BloomFilter.__init__(self, array, k, seedLimit)

class StandardBloomFilter(BloomFilter):
    def __init__(self, n, k, seedLimit = 1000):
        array = BitArray(n)
        BloomFilter.__init__(self, array, k, seedLimit)

def playWithFilter(n, k = 2):
    bf = StandardBloomFilter(n, 2)
    v1 = "rawrawrawrawrawrawrawrawr"
    bf.insert(v1)
    print "Contains an unequal string?", bf.contains("the opposite of rawr rawr")
    print "Contains the original string?", bf.contains(v1)
    print bf.array

    b2 = DecayingBloomFilter(n, 2, 0.5)
    b2.insert(v1)
    print b2.array
    time.sleep(2)
    print b2.array

def findCollision(n, k = 2):
    bf = StandardBloomFilter(n, 2)
    test = "Hello world"
    bf.insert(test)
    print bf.contains(test)
    found = False
    val = ""
    while not found: # terrible collision search
        val = (''.join(random.choice(string.ascii_uppercase) for i in range(128)))
        if bf.contains(val):
            print "Found collision", test, val
            found = True
    return test, val

def main(args):
    n = int(args[1])
    k = int(args[2])

    # stupid tests...
    playWithFilter(n, k)
    # findCollision(n, k)

    return

if __name__ == "__main__":
    main(sys.argv)
