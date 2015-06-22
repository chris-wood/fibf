import os
import sys
import random
import time
# from joblib import Parallel, delayed
from bloom import *

minimumTimeUnit = 1000 # milliseconds
sequenceNumber = 1

def sampleExp(mean):
    u = random.random() # [0.0, 1.0)
    x = (-1 * math.log(1 - u)) / float(mean)
    return int(math.ceil(x))

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
    decayRate = float(args[3]) / minimumTimeUnit    # per second
    arrivalRate = float(args[4]) / minimumTimeUnit  # per second
    deleteRate = float(args[5]) / minimumTimeUnit # per second
    randomSampleSize = int(args[6])

    bf = CountingBloomFilter(filterSize, filterHashes)

    contents = []
    falsePositives = {}
    falseNegatives = {}
    counts = {}

    decayCounter = sampleExp(decayRate)
    deleteCounter = sampleExp(deleteRate)
    arrivalCounter = sampleExp(arrivalRate)

    print decayCounter, deleteCounter, arrivalCounter

    for t in range(timeSteps):
        if decayCounter == 0: # decay algorithm here...
            decayCounter = sampleExp(decayRate)
            deleteFromFilter(bf)
        if arrivalCounter == 0: # add a random new content to the set
            arrivalCounter = sampleExp(arrivalRate)
            randomContent = generateNewContent()
            contents.append(randomContent)
        if deleteCounter == 0: # pick random element in content, delete it, remove it from contents
            deleteCounter = sampleExp(deleteRate)
            if len(contents) > 1:
                target = random.sample(contents, 1)[0]
                bf.delete(target)

        decayCounter -= 1
        arrivalCounter -= 1
        deleteCounter -= 1

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

        print >> sys.stderr, "Time %d %f %f %d" % (t, end - start, fp, counts[t])

    for t in range(timeSteps):
        fp = float(len(falsePositives[t])) / randomSampleSize
        fn = float(len(falseNegatives[t])) / randomSampleSize
        print "%d,%f,%f,%d" % (t, fp, fn, counts[t])

if __name__ == "__main__":
    main(sys.argv[1:])
