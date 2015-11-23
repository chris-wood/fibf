import os
import sys
import random
import math
import time
from scaling_timing_bloom_filter import ScalingTimingBloomFilter
from timing_bloom_filter import TimingBloomFilter
import tornado.ioloop
import tornado.testing
import time
from utils import TimingBlock, TestFile

# from bloom import *

minimumTimeUnit = 1000 # milliseconds
sequenceNumber = 1

def sampleExp(rate):
    u = random.random() # [0.0, 1.0)
    x = (-1 * math.log(1 - u)) * float(rate)
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

# NOTE: this does not model the cache (i.e., it assumes the router does not
# have a cache, so everything goes into the filter)

def run_experiment(stbf, filter_type, args):
    global minimumTimeUnit

    timeSteps = int(args[0]) # number of epochs (could be ns, us, ms, or s)
    initialFilterSize = int(args[1])
    decayRate = float(args[2]) #  # per second
    arrivalRate = float(args[3]) # / minimumTimeUnit  # per second
    deleteRate = float(args[4]) # / minimumTimeUnit # per second
    randomSampleSize = int(args[5])

    contents = []
    falsePositives = {}
    falseNegatives = {}
    counts = {}

    deleteCount = sampleExp(deleteRate)
    arrivalCount = sampleExp(arrivalRate)

    for t in range(timeSteps):
        start = time.time()
        stbf.step()

        for i in range(arrivalCount):
            randomContent = generateNewContent()
            contents.append(randomContent) # now in the set
            stbf += randomContent
        # print >> sys.stderr, "DELETE %d" % (deleteCount)
        for i in range(deleteCount):
            if len(contents) > 1:
                target = random.sample(contents, 1)[0]
                # stbf.remove(target) # doh!
                stbf.removeRandom() # this decrements *every* slot randomly...
                # contents.remove(target) # no longer actually in the set

        arrivalCount = sampleExp(arrivalRate) # number of arrivals in each epoch
        deleteCount = sampleExp(deleteRate) # number of deletions (randomly sampled) in each epoch

        falsePositives[t] = []
        falseNegatives[t] = []

        # Check to see if decays deleted existing items from the filter
        random.shuffle(contents)
        for content in contents[:randomSampleSize]:
            if not stbf.contains(content):
                falseNegatives[t].append(content)

        # Check the false positive rate (by randomly generated samples)
        randomContents = generateRandomContent(randomSampleSize)
        for randomElement in randomContents:
            element = randomElement + "/" + str(os.urandom(10))
            if element not in contents and stbf.contains(element):
                # print >> sys.stderr, "Found false positive :( %s" % (element)
                falsePositives[t].append(element)

        end = time.time()

        fp = float(len(falsePositives[t])) / randomSampleSize
        fn = float(len(falseNegatives[t])) / randomSampleSize
        counts[t] = len(contents)

        # if t % 100 == 0:
        print >> sys.stderr, "%s,%d,%f,%f,%f,%d" % (filter_type, t, end - start, fp, fn, counts[t])

    for t in range(timeSteps):
        fp = float(len(falsePositives[t])) / randomSampleSize
        fn = float(len(falseNegatives[t])) / randomSampleSize
        print "%s,%d,%f,%f,%d" % (filter_type, t, fp, fn, counts[t])

def main(args):
    timeSteps = int(args[0]) # number of epochs (could be ns, us, ms, or s)
    initialFilterSize = int(args[1])
    decayRate = float(args[2]) #  # per second
    arrivalRate = float(args[3]) # / minimumTimeUnit  # per second
    deleteRate = float(args[4]) # / minimumTimeUnit # per second
    randomSampleSize = int(args[5])

    stbf = ScalingTimingBloomFilter(initialFilterSize, decay_time=decayRate).start()
    run_experiment(stbf, "ScalingTiming", args)

    # Timing BF is not run because it takes far too long to index
#    stbf = TimingBloomFilter(initialFilterSize, decay_time=decayRate).start()
#    run_experiment(stbf, "Timing", args)

def test():
    stbf = ScalingTimingBloomFilter(500, decay_time=4).start()
    n = 100
    for i in xrange(2*n):
        stbf.add("idx_%d" % i)

    for i in xrange(2*n):
        if not stbf.contains("idx_%d" % i):
            print "WTF 1 %d" %(i)

    stbf.step()
    stbf.step()
    stbf.step()
    # stbf.step()

    for i in xrange(2*n):
        if not stbf.contains("idx_%d" % i):
            print "WTF 2 %d" %(i)

    stbf.step()
    for i in xrange(2*n):
        if stbf.contains("idx_%d" % i):
            print "WTF 3 %d" %(i)

    print "done"

if __name__ == "__main__":
    if len(sys.argv) == 1:
        for i in range(100):
            print i, sampleExp(i)
        test()
    else:
        main(sys.argv[1:])
