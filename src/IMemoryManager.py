
class IMemoryManager:
    def __init__(self, nodeNum):
        self.temp = None
        self.childVec = [None] * 8
        self.current = 0
        self.child_current = 0
        self.prior = 0
        self.maxNum = nodeNum
    
    def get_Instance(self):
        return self.temp
    
    def get_children(self):
        return self.childVec
    
    def dealloc(self):
        pass
    
    def getCurrent(self):
        return self.current
    
    def getChildCurrent(self):
        return self.child_current
    
    def setCurrent(self, x):
        self.current = x
    
    def setChildCurrent(self, x):
        self.child_current = x
    
    def takeAPicture(self):
        pass
    
    def restore(self):
        pass
    
    def swap(self, swapper):
        pass
