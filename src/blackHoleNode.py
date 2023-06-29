import numpy as np
import constantly as const
import random

class node:
    def __init__(self, nodeId, ep):
        self.nodeId = nodeId
        self.points = np.array([0.0] * const.DIM)
        for i in range(const.DIM):
            self.points[i] = (float(random.randint(0, 2147483647))/32767.0) - 0.5
        self.clusterId = -1
        self.degree = 1
        self.ep = np.array([ep])



    def getID(self) -> int:
        return self.nodeId
    
    def setValue(self, point, idx):
        self.points[idx] = float(point)

    def getValues(self) -> np.array:
        return self.points
    
    def getValue(self, idx) -> float:
        return self.points[idx]
    
    def setDegree(self, degree):
        self.degree = degree

    def getDegree(self) -> int:
        return self.degree
    
    def setCluster(self, clusterId):
        self.clusterId = clusterId

    def getCluster(self) -> int:
        return self.clusterId
    
    def getEdgeSet(self) -> np.array:
        return self.ep
    
    def setEdge(self, id):
        self.ep = np.append(self.ep, id)
    
    def findEdge(self, origin, id)  -> bool:
        x = np.where(self.ep == id)
        return x != np.array([])
    

    def isnot_labeled(self) -> bool:
        return self.clusterId == -1