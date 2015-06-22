import os
import sys
import random
import time
# from joblib import Parallel, delayed
from bloom import *

minimumTimeUnit = 1000 # milliseconds
sequenceNumber = 1

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def deleteFromFilter(bf):
    pass

def generateNewContent():
    global sequenceNumber
    name = "lci:/random/" + str(sequenceNumber)
    sequenceNumber += 1
    return name

def generateRandomContent(n):
    contents = []
    for i in range(n):
        contents.append(generateNewContent())
    return contents

# NOTE: this does not model the cache (i.e., it assumes the router does not have a cache)
def main(args):
    global minimumTimeUnit

    timeSteps = int(args[0]) * minimumTimeUnit # epochs (input is seconds and then multiplied by the MTU)
    filterSize = int(args[1])
    filterHashes = int(args[2])
    decayInterval = int(args[3])
    arrivalRate = int(args[4]) # per second
    deletionRate = int(args[5]) # per second
    randomSampleSize = int(args[6])

    arrivalInterval = int(float(1 / float(arrivalRate)) * minimumTimeUnit)
    deletionInterval = int(float(1 / float(deletionRate)) * minimumTimeUnit)

    print >> sys.stderr, "Arrival info", arrivalRate, arrivalInterval
    print >> sys.stderr, "Deletion info", deletionRate, deletionInterval

    bf = CountingBloomFilter(filterSize, filterHashes)

    contents = []
    falsePositives = {}
    falseNegatives = {}
    counts = {}

    # TODO: create counter for arrival and deletion based on poisson process

    for t in range(timeSteps):
        if (t % decayInterval) == 0: # decay algorithm here...
            deleteFromFilter(bf)
        if (t % arrivalInterval) == 0: # add a random new contnet to the set
            randomContent = generateNewContent()
            contents.append(randomContent)
        if (t % deletionInterval) == 0: # pick random element in content, delete it, remove it from contents
            if len(contents) > 1:
                target = random.sample(contents, 1)[0]
                bf.delete(target)

        falsePositives[t] = []
        falseNegatives[t] = []

        start = time.time()

        # Check to see if decays deleted existing items from the filter
        for content in contents:
            if not bf.contains(content):
                falseNegatives[t].append(content)

        # Check the false positive rate (by randomly generated samples)
        randomContents = generateRandomContent(randomSampleSize)
        for randomElement in randomContents:
            element = randomElement + str(os.urandom(1))
            if bf.contains(element):
                falsePositives[t].append(element)

        end = time.time()

        fp = float(len(falsePositives[t])) / randomSampleSize
        counts[t] = len(contents)

        print >> sys.stderr, "Time %d %f %f" % (t, end - start, fp, len(counts)

    for t in range(timeSteps):
        fp = float(len(falsePositives[t])) / randomSampleSize
        fn = float(len(falseNegatives[t])) / randomSampleSize
        print "%d,%f,%f,%d" % (t, fp, fn, counts[t])

if __name__ == "__main__":
    main(sys.argv[1:])

