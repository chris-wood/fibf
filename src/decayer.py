import sys
import random
from bloom import *

minimumTimeUnit = 1000 # milliseconds
sequenceNumber = 1

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

# NOTE: this does not model the cache
def main(args):
    global minimumTimeUnit

    timeSteps = int(args[0]) * minimumTimeUnit # epochs (input is seconds and then multiplied by the MTU)
    filterSize = int(args[1])
    filterHashes = int(args[2])
    decayInterval = int(args[3])
    arrivalRate = int(args[4]) # per second
    arrivalInterval = int(float(1 / float(arrivalRate)) * minimumTimeUnit)
    deletionRate = int(args[5]) # per second
    deletionInterval = int(float(1 / float(deletionRate)) * minimumTimeUnit)
    randomSampleSize = int(args[6])

    print arrivalRate, arrivalInterval

    bf = CountingBloomFilter(filterSize, filterHashes)

    contents = []
    falsePositives = {}
    falseNegatives = {}
    for t in range(timeSteps):
        if (t % decayInterval) == 0:
            # decay algorithm here...
            deleteFromFilter(bf)
        if (t % arrivalInterval) == 0:
            # add a random new contnet to the set
            randomContent = generateNewContent()
            contents.append(randomContent)
        if (t % deletionInterval) == 0:
            # pick random element in content, delete it, remove it from contents
            target = random.sample(contents, 1)[0]
            bf.delete(target)

        falsePositives[t] = []
        falseNegatives[t] = []

        for content in contents:
            if not bf.contains(content):
                falseNegatives[t].append(content)
            randomContents = generateRandomContent(randomSampleSize)
            for randomElement in randomContents:
                if bf.contains(randomElement):
                    falsePositives[t].append(randomElement)    
     
    
    for t in range(timeSteps):
        fp = float(len(falsePositives)) / randomSampleSize
        fn = float(len(falseNegatives)) / randomSampleSize
        print t, fp, fn
        
if __name__ == "__main__":
    main(sys.argv[1:])