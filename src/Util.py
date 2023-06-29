
import constantly as const
import math

def calcDist_DIM(a , b):
    sum = 0.0
    for i in range(const.DIM):
        sum = sum + ((a[i] - b[i]) * (a[i] - b[i]))
    return math.sqrt(sum)
    