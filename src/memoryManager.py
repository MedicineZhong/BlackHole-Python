import math
import constantly as const
from IMemoryManager import IMemoryManager
from IOctTree import IOctTree

class memoryManager(IMemoryManager):

    def __init__(self, nodeNum):
        self.current = 0
        self.child_current = 0
        self.maxNum = nodeNum * 12
        self.prior = -1
        self.temp = [IOctTree() for _ in range(self.maxNum)]
        self.childVec = [[] for _ in range(self.maxNum)]

        for i in range(self.maxNum):
            self.childVec[i] = [IOctTree()] * int(math.pow(2, const.DIM))

    def get_children(self):
        self.child_current += 1
        return self.childVec[self.child_current - 1]


    def get_child_current(self) -> int:
        return self.child_current
    
    def set_child_current(self, val):
        self.child_current = val

    def get_Instance(self) -> IOctTree:
        self.current += 1
        return self.temp[self.current - 1]

    def get_current(self) -> int:
        return self.current
    
    def set_current(self, val):
        self.current = val


    def takeAPicture(self):
        self.prior = self.current

    def restore(self):
        self.current = self.prior
        self.child_current = self.prior

    # def swap(self, swapper):
    #     if(self.current == self.prior and self.prior == -1):
    #         return
        
    #     self.prior += 1
    #     s = swapper
    #     swapper