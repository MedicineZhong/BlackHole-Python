import math
import numpy

class exponentVar:
    
    def __init__(self, a, r, degree: int):
        self.attrExponent = a
        self.repuExponent = r
        self.finalAttrExponent = self.attrExponent
        self.finalRepuExponent = self.repuExponent

        sumOfDegree = degree
        density =  numpy.float64(1.0) / sumOfDegree
        self.repuFactor = density * math.pow(sumOfDegree, 0.5*(self.attrExponent - self.repuExponent))

    def getAttrExponent(self):
        return self.attrExponent
    
    def getRepuExponent(self):
        return self.repuExponent
    
    def getFinalAttrExponent(self):
        return self.finalAttrExponent
    
    def getFinalRepuExponent(self):
        return self.finalRepuExponent
    
    def getRepuFactor(self):
        return self.repuFactor
    
    def setAttrExponent(self, val):
        self.attrExponent = val

    def setRepuExponent(self, val):
        self.repuExponent = val

    def setFinalAttrExponent(self, val):
        self.finalAttrExponent = val

    def setFinalRepuExponent(self, val):
        self.finalRepuExponent = val

    def setRepuFactor(self, val):
        self.repuFactor = val

    
    
        