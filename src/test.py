import string
import random
import hashlib
from Crypto.Cipher import AES

def sxor(s1,s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def randomString(length):
	return (''.join(random.choice(string.ascii_uppercase) for i in range(length)))

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

# router computes this when inserting into FIB
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


