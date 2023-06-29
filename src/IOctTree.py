
class IOctTree:
    MAX_DEPTH = 18
    
    # def __init__(self):
    #     self.node = None
    #     self.children = []
    #     self.childCount = 0
    #     self.childLength = 0
    #     self.position = None
    #     self.weight = 0.0
    #     self.minPos = None
    #     self.maxPos = None
    
    def __del__(self):
        pass
    
    def __init__(self, node = None, position = None, minPos = None, maxPos = None):
        self.node = node
        self.children = []
        self.childCount = 0
        self.childLength = 0
        self.position = position
        self.weight = 0.0
        self.minPos = minPos
        self.maxPos = maxPos
    
    def setElement(self, node, position, minPos, maxPos, mgr):
        self.node = node
        self.children = []
        self.childCount = 0
        self.childLength = 0
        self.position = position
        self.weight = 0.0
        self.minPos = minPos
        self.maxPos = maxPos
    
    def getPosX(self):
        return self.position[0]
    
    def getPosY(self):
        return self.position[1]
    
    def getValues(self):
        return self.position
    
    def getNode(self):
        return self.node
    
    def getLength(self):
        return self.childLength
    
    def LengthIncrease(self):
        self.childLength += 1
    
    def getWeight(self):
        return self.weight
    
    def getUsed(self):
        return self.node is not None
    
    def addNode(self, newNode, newPos, depth, mgr):
        pass
    
    def addNode2(self, newNode, newPos, depth, mgr, st):
        pass
    
    def getWidth(self):
        return self.maxPos[0] - self.minPos[0]
    
    def getHeight(self):
        return self.maxPos[1] - self.minPos[1]
    
    def removeNode(self, oldNode, oldPos, depth, mgr):
        pass
    
    def clearMemory(self):
        pass
    
    def clearMemory(self, p):
        pass
