import math

import constantly as const
from octTree import octTree
from exponentVar import exponentVar
import numpy as np
from blackHoleNode import node as blackHoleNode
import Util

class nodeCollection:

    def __init__(self):
        self.nodeMap = {}
        self.nodeVec = []
        self.degMat = None
        self.adjMat = None

    def putNode(self, nNodeId : int, other:int):
        if(self.degMat[nNodeId - 1] == 0):
            self.degMat[nNodeId - 1] = self.degMat[nNodeId - 1] + 1
            newNode = blackHoleNode(nNodeId, other)
            self.nodeMap[nNodeId] = newNode
        
        else:
            if(self.nodeMap[nNodeId].findEdge(nNodeId, other) == False):
                self.degMat[nNodeId - 1] = self.degMat[nNodeId - 1] + 1
                self.nodeMap[nNodeId].setEdge(other)
    
    #Todo: check if this is correct
    def copyToVector(self):
        self.nodeVec = list(self.nodeMap.values())
        self.nodeVec.sort(key=lambda x: x.getID())


    def setAdjMat(self, maxValue):
        len = maxValue + 1
        for i in range(len):
            for j in range(len):
                self.adjMat[i][j] = 0

    def setDegMat(self, maxValue):
        len = maxValue
        self.degMat = np.zeros(len)
        for i in range(len):
            self.degMat[i] = 0

    def checkEdge(self, id1_notMinus, id2_notMinus) -> bool:
        return self.adjMat[id1_notMinus][id2_notMinus] != 0
    
    def getSumOfDegree(self):
        s = 0
        for node in self.nodeVec:
            s += node.getDegree()
        return s
    
    def findInitEnergy(self, expVar: exponentVar, octTree: octTree) -> float:
        sum = 0
        for i in range(len(self.nodeVec)):
            sum += self.getEnergy(self.nodeVec[i], expVar, octTree)
        return sum
    
    def degreeSet(self):
        for i in range(len(self.nodeVec)):
            self.nodeVec[i].setDegree(self.degMat[i])

    def getNodeVec(self) -> np.array:
        return self.nodeVec
    
    def getNodeMap(self) -> np.array:
        return self.nodeMap
    
    def getEnergyR(self, unp: blackHoleNode, expVar:exponentVar, tree:octTree) -> float:
        if(tree == None or unp.getDegree() == 0):
            return 0.0
        
        if(tree.node == unp):
            return 0.0
        
        repuExponent = expVar.getRepuExponent()	
        repuFactor = expVar.getRepuFactor()

        pos = unp.getValues()
        pos2 = tree.getValues()

        treeWidth = tree.getWidth()
        dist = Util.calcDist_DIM(pos, pos2)
        if(dist == 0.0):
            return 0.0
        
        if(tree.childCount > 0 and dist < 1.0 * treeWidth):
            energy = 0.0
            for i in range(tree.getLength()):
                energy += self.getEnergyR(unp, expVar, tree.children[i])
            return energy
        
        if(repuExponent == 0.0):
            return -1.0 * repuFactor * unp.getDegree() * tree.getWeight() * math.log(dist)
        else:
            return -1.0 * repuFactor * unp.getDegree() * tree.getWeight() * math.pow(dist, repuExponent) / repuExponent
        

    def getEnergyAA(self, unp: blackHoleNode, expVar:exponentVar, tree:octTree) -> float:
        attrExponent = expVar.getAttrExponent()


        pos = unp.getValues()
        edgeList = unp.getEdgeSet()

        energy = 0.0

        for i in range(len(edgeList)):
            value = edgeList[i] - 1
            pos2 = self.nodeVec[value].getValues()
            dst = Util.calcDist_DIM(pos, pos2)
            if(attrExponent == 0.0):
                energy += math.log(dst)
            else:
                energy += math.pow(dst, attrExponent) / attrExponent

        return energy
    
    def getEnergy(self, unp: blackHoleNode, expVar:exponentVar, tree:octTree) -> float:
        gr = self.getEnergyR(unp, expVar, tree)
        ga = self.getEnergyAA(unp, expVar, tree)

        return ga + gr
    

    def addRepulsionDir(self, unp: blackHoleNode, dir:np.array,expVar:exponentVar, tree:octTree) -> float:
        if(tree == None or tree.node == unp):
            return 0.0
        
        if(unp.getDegree() == 0):
            return 0.0
        
        repuExponent = expVar.getRepuExponent()
        repuFactor = expVar.getRepuFactor()

        pos = unp.getValues()
        pos2 = tree.getValues()
        dist = Util.calcDist_DIM(pos, pos2)

        if(dist == 0.0):
            return 0.0
        
        if(tree.childCount > 0 and dist < 1.0 * tree.getWidth()):
            for i in range(tree.getLength()):
                self.addRepulsionDir(unp, dir, expVar, tree.children[i])
            return 0.0
        
        temp = repuFactor * unp.getDegree() * tree.getWeight() * math.pow(dist, repuExponent - 2.0)

        for z in range(const.DIM ):
            dir[z] -= temp * (pos2[z] - pos[z])

        return temp * abs(repuExponent - 1)
    
    def addAttractionDirA(self, unp: blackHoleNode, dir:np.array,expVar:exponentVar, tree:octTree) -> float:
        attrExponent = expVar.getAttrExponent()

        if(unp.getDegree() == 0):
            return 0.0
        
        pos = unp.getValues()
        edgeList = unp.getEdgeSet()

        for i in range(len(edgeList)):
            value = edgeList[i] - 1
            pos2 = self.nodeVec[value].getValues()
            dst = Util.calcDist_DIM(pos, pos2)
            if(dst == 0.0):
                continue
            
            temp = math.pow(dst, attrExponent - 2.0)
            for z in range(const.DIM):
                dir[z] += temp * (pos2[z] - pos[z])

        return 0.0
    
    def setDir(self, unp: blackHoleNode, dir:np.array,expVar:exponentVar, tree:octTree):
        self.addRepulsionDir(unp, dir, expVar, tree)
        self.addAttractionDirA(unp, dir, expVar, tree)
