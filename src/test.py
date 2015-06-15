import sys
import string
import random
import hashlib
from Crypto.Cipher import AES

def sxor(s1,s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def randomString(length):
	return (''.join(random.choice(string.ascii_uppercase) for i in range(length)))

class Interest(object):
    def __init__(self, name):
        self.name = name

class ContentObject(object):
    def __init__(self, name):
        self.name = name

class RouterMessage(object):
    def __init__(self):
        pass

class Forwarder(object):
    def __init__(self):
        self.fib = FIB()
        self.cs = ContentStore()

class HashTable(object):
    def __init__(self):
        self.table = {}

    def insert(self, key, val):
        self.table[key] = val

    def contains(self, index):
        return index in self.table

    def retrieve(self, index):
        if self.contains(index):
            return self.table[index]

class ContentStore(HashTable):
    pass # a content store is just a glorified hash table

class FIB(HashTable):
    def __init__(self):
        HashTable.__init__(self)
        self.indexKey = randomString(16)
        self.insertIV = randomString(16)

    def _insertPrefix(self, prefix, IV):
        padLength = len(prefix) % 16
        prefix = prefix + (" " * (16 - padLength)) if padLength > 0 else prefix
        inserter = AES.new(self.indexKey, AES.MODE_CBC, IV)
        return inserter.encrypt(prefix)

    def insert(self, key, val):
        components = key.split("/")
        for index, component in enumerate(components):
            prefix = self._insertPrefix("/".join(components[0: index + 1]), self.insertIV)
            super(FIB, self).insert(prefix, val)

    def _findMatches(self, indexValue, IV):
        components = indexValue.split("/")
        matches = []
        for index, component in enumerate(components):
            if index == 0:
                continue # the empty name
            plaintext = "/".join(components[0:index + 1])
            prefix = self._insertPrefix(plaintext, IV)
            if super(FIB, self).contains(prefix):
                matches.append(prefix)
   
        if super(FIB, self).contains(indexValue):
            matches.append(indexValue)

        return matches

    def containsPrefix(self, index, IV):
        return len(self._findMatches(index, IV)) > 0

    def lookup(self, index, IV):
        matches = self._findMatches(index, IV)
        values = []
        for match in matches:
            value = super(FIB, self).retrieve(match)
            values.append((match, value))
        return values 

    def containsFullName(self, index, IV):
        prefix = self._insertPrefix(index, IV)
        return super(FIB, self).contains(prefix)

# Test the forwarder FIB
f1 = Forwarder()
name1 = "/a/b/c"
name2 = "/a/b/d"
print "Inserting %s" % (name1)
f1.fib.insert(name1, 0)
print "Does the FIB contain the prefix for %s ?" % (name2),
print f1.fib.containsPrefix(name2, f1.fib.insertIV)
print "These are the prefixes (in their encoded form) ",
print f1.fib.lookup(name2, f1.fib.insertIV)
print "Does it contain the full name %s ? " % (name2),
print f1.fib.containsFullName(name2, f1.fib.insertIV)

# Create a new random name that maps to name1, using a different IV
randomIV = randomString(16)
decrypter = AES.new(f1.fib.indexKey, AES.MODE_CBC, randomIV)
ciphertext = f1.fib._insertPrefix(name1, f1.fib.insertIV)
print "Generating a new random representation of the target name %s..." % (name1)
randomName = decrypter.decrypt(ciphertext)
print "We got %s" % (randomName)

print "Does the FIB contain this new random name %s? " % (randomName),
print f1.fib.containsFullName(randomName, randomIV)

# Verify that name1 \not= randomname
print "Are these names equal?"
print name1, randomName, name1 == randomName
print "Definitely not!"




###### TODO:
# 1. This procedure is done for every component in the name
# 2. Add this cache support

###### NOTES:
# 1. PIT still contains provided name and IV
# 2. The cache is indexed by hash of the name
# 3. Interest payload contains the encrypted version of the interest name and additional data

###### QUESTIONS:
# 1. Is this different (used in addition to, better than?) than l2 encryption?
# 2. What are the benefits aside from per-hop name switching? [it hides the routable name prefix]

def test():
    # routecomputes this when inserting into FIB
    fibKEY = 'This is a key123' # permanent key for the router 
    fibIV = 'This is an IV456' # IV used when inserting into the FIB, fixed
    fibData = randomString(16)

    print "Start data:", fibData, fibIV
    encryption_suite = AES.new(fibKEY, AES.MODE_CBC, fibIV)
    cipher_textA = encryption_suite.encrypt(fibData)

    # router gives us IV and KEY, we compute the expected value of the actual message
    actualMessage = fibData # we got this from an interest
    encryption_suite = AES.new(fibKEY, AES.MODE_CBC, fibIV)
    cipher_textB = encryption_suite.encrypt(actualMessage)

    print "Values:", fibData, actualMessage
    print "Equal ciphertext?", cipher_textA == cipher_textB

    # now we make a new random IV, use it to decrypt the expected ciphertext from the
    # router, and then use that new plaintext as our new value
    newIV = randomString(16)
    decrypter = AES.new(fibKEY, AES.MODE_CBC, newIV)
    newData = decrypter.decrypt(cipher_textB)

    print "New data:", newData, newIV # IV to use when indexing into the FIB

    ## now we send the new plaintext and IV to the router

    # the router uses the newData and newIV to index into the FIB
    encrypter = AES.new(fibKEY, AES.MODE_CBC, newIV)
    indexedCiphertext = encrypter.encrypt(newData)
    print "Correct output?", indexedCiphertext == cipher_textA


