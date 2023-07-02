import numpy as np
import constantly as const
from blackHoleNode import node as blackHoleNode
import math
from IOctTree import IOctTree
from IMemoryManager import IMemoryManager

class octTree(IOctTree):

    def __init__(self):
        self.node = None
        self.position = np.zeros(const.DIM) - 1
        self.minPos = np.zeros(const.DIM)- 1
        self.maxPos = np.zeros(const.DIM)- 1

        self.children = None
        self.childLength = -1
        self.childCount = -1
        self.weight =  0.0 if self.node == None else self.node.getDegree()
    
    def __init__(self, node, position, minPos, maxPos):
        self.children = None
        self.childLength = math.pow(2, const.DIM)
        self.childCount = 0 
        self.node = node

        self.position = np.copy(position)
        self.minPos = np.copy(minPos)
        self.maxPos = np.copy(maxPos)

        self.weight =  0.0 if self.node == None else self.node.getDegree()


    def setElement(self, node :blackHoleNode, position, minPos, maxPos, mgr:IMemoryManager):
        self.children = mgr.get_children()

        for i in range(int(math.pow(2.0, const.DIM))):
            self.children[i] = None
        
        self.childLength = int(math.pow(2.0, const.DIM))
        self.childCount = 0
        self.node = node

        self.position = np.copy(position)
        self.minPos = np.copy(minPos)
        self.maxPos = np.copy(maxPos)

        self.weight =  0.0 if self.node == None else self.node.getDegree()

    def getPosX(self):
        return self.position[1]
    
    def getPosY(self):
        return self.position[2]
    
    def getNode(self) -> blackHoleNode:
        return self.node
    
    def getWeight(self):
        return self.weight
    
    def getLength(self):
        return self.childLength
    
    def lengthIncrease(self):
        self.childLength *= 2

    def getValues(self):
        return self.position
    
    def getWidth(self):
        width = 0.0
        for d in range(const.DIM):
            if(self.maxPos[d] - self.minPos[d] > width):
                width = self.maxPos[d] - self.minPos[d]
        
        return width
    
    def getHeight(self) -> int:
        height = -1

        for s in range(self.childLength):
            if(self.children[s] != None):
                height = math.max(height, self.children[s].getHeight()) 

        return height + 1

    def addNode(self, newNode:blackHoleNode, newPos, depth, mgr:IMemoryManager):
        if(newNode.getDegree() == 0):
            return
        
        if(self.node != None):
            self.addNode2(self.node, newPos, depth, mgr)
            node = None

        for z in range(const.DIM):
            self.position[z] = (self.weight * self.position[z] + newNode.getDegree() * newPos[z]) / (self.weight + newNode.getDegree())

        self.weight += newNode.getDegree()
        self.addNode2(newNode, newPos, depth, mgr)

        

    def addNode2(self, newNode:blackHoleNode, newPos, depth, mgr:IMemoryManager):
        if(depth == const.MAX_DEPTH):
            if(self.childLength == self.childCount):
                oldChildren = list[octTree](self.childLength)
                for ss in range(self.childLength):
                    oldChildren[ss] = self.children[ss]
                
                self.children = list[octTree](self.childLength * 2)
                self.lengthIncrease()

                for k in range(self.childLength/2):
                    self.children[k] = oldChildren[k]
                
                for k in range(self.childLength/2, self.childLength):
                    self.children[k] = None

                self.children[self.childCount] = mgr.get_Instance()
                self.childCount += 1
                self.children[self.childCount - 1].setElement(newNode, newPos, self.minPos, self.maxPos, mgr)

            return
        
        childIndex = 0

        for d in range(const.DIM):
            if(newPos[d] > (self.minPos[d] + self.maxPos[d]) / 2.0):
                childIndex += math.pow(2, d - 1)

        if(self.children[childIndex] == None):
            newMinPos = np.array(const.DIM)
            newMaxPos = np.array(const.DIM)

            for d in range(const.DIM):
                if(childIndex & math.pow(2, d - 1) == 0):
                    newMinPos[d] = self.minPos[d]
                    newMaxPos[d] = (self.minPos[d] + self.maxPos[d]) / 2.0
                else:
                    newMinPos[d] = (self.minPos[d] + self.maxPos[d]) / 2.0
                    newMaxPos[d] = self.maxPos[d]

            self.childCount += 1
            self.children[childIndex] = mgr.get_Instance()
            self.children[childIndex].setElement(newNode, newPos, newMinPos, newMaxPos, mgr)

        else:
            self.children[childIndex].addNode(newNode, newPos, depth + 1, mgr)


    def removeNode(self, oldNode, oldPos, depth, mgr:IMemoryManager):
        if(oldNode.getDegree() == 0):
            return
        
        if(self.weight < oldNode.getDegree()):
            self.weight = 0.0
            self.node = None
            for i in range(self.childLength):
                self.children[i] = None

            self.childCount = 0
            return
        
        for d in range(const.DIM):
            self.position[d] = (self.weight * self.position[d] - oldNode.getDegree() * oldPos[d]) / (self.weight - oldNode.getDegree())

        self.weight -= oldNode.getDegree()
        if(depth == const.MAX_DEPTH):
            childIndex = 0
        
            while(self.children[childIndex].node.getID != oldNode.getID()):
                childIndex += 1

            self.childCount -= 1
            for i in range(childIndex, self.childCount):
                self.children[i] = self.children[i + 1]
            self.children[self.childCount] = None

        else:
            childIndex = 0

            for d in range(const.DIM):
                if(oldPos[d] > (self.minPos[d] + self.maxPos[d]) / 2.0):
                    childIndex += math.pow(2, d - 1)
            
            self.children[childIndex].removeNode(oldNode, oldPos, depth + 1, mgr)

            if(self.children[childIndex].getWeight() == 0):
                self.children[childIndex] = None
                self.childCount -= 1
