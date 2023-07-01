import os
import sys
import random
from datetime import datetime
from ClusterPlay import ClusterPlay
from DBscanPlay import DBscanPlay
import constantly as const

if len(sys.argv) < 6:
    sys.argv = ["", "./Data/50000/community.dat", "2", "0.01", "5", "0.1"]
    
    # sys.stderr.write("Error occurred! please check the usage!\n")
    # sys.stderr.write("usage: python BlackHole.py [Input] [Dimension] [Alpha] [MinPTS] [PruningPercents]\n")
    # sys.stderr.write("example: python BlackHole.py ../Data/football.dat 2 0.01 5 0.1\n")
    # sys.exit(-1)

random.seed(datetime.now())

# Input parameter processing
alpha = float(sys.argv[3])
print("alpha =", alpha)
const.DIM = int(sys.argv[2])
print("dimens =", const.DIM)
minPts = int(sys.argv[4])
print("minpts =", minPts)
pruningFraction = float(sys.argv[5])
print("priningFactor =", pruningFraction)

cp = ClusterPlay()

print(os.getcwd())
print(os.path.exists(sys.argv[1]))

fileName = sys.argv[1] + "_dimsnsion_" + sys.argv[2] + "_alpha_" + sys.argv[3] + "_minPts_" + sys.argv[4] + "_pruningFactor_" + sys.argv[5] + "_position.out"

cp.play(sys.argv[1], alpha, sys.argv[3], fileName)

# DBSCAN
dbc = DBscanPlay()
dbc.dbscanCalculator(inputFile = fileName,minPts = minPts, removePercentage = pruningFraction/100.0)

sys.exit(0)
