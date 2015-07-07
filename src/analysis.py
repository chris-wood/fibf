import math
import sys

def comb(n, k):
    return (math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))

def probEmpty(m, k, n):
    return (1 - (1 / float(m))) ** (k * n)

def falsePositive(m, k, n):
    inner = (1 - (1 / float(m)))
    inner = (1 - inner**(k * n)) ** k
    return inner

def falseNegative(m, k, n):
    acc = 0
    for i in range(1, k + 1):
        emptyProb = probEmpty(m, k, n)
        nonEmptyProb = 1 - emptyProb
        reduction = (1 - (1 - (float(i) / (float(m) * nonEmptyProb))) ** k)
        prob = comb(k, i) * (emptyProb ** i) * (nonEmptyProb ** (k - i)) * reduction
        acc += prob
    return acc

args = sys.argv[1:]
m = int(args[0])
k = int(args[1])
nmax = int(args[2])

for i in range(1, nmax):
    fp = falsePositive(m, k, i)
    fn = falseNegative(m, k, i) 
    print i, fp, fn


