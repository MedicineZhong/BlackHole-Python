

import time
from edgeReader import edgeReader
from exponentVar import exponentVar
from memoryManager import memoryManager
from nodeCollection import nodeCollection
import constantly as const
from octTree import octTree


class ClusterPlay:

    def play(self, inputfile :str, alpha:float,alphaChar:str,fileFullName:str):
        iter = 100

        fr = edgeReader()
        nc = nodeCollection()

        fr.readFile(inputfile, nc)

        print("Check it!")
        nc.copyToVector()
        nc.degreeSet()

        expVar = exponentVar(alpha, 0.0, nc.getSumOfDegree())
        memMgr = memoryManager(len(nc.getNodeVec()))

        tt = self.buildOctTree(nc, memMgr)
        vecp = nc.getNodeVec()

        #To get initial energy
        initEnergy = 0.0
        for k in range(len(vecp)):
            initEnergy += nc.getEnergy(vecp[k], expVar, tt)

        print("Initial Energy: ", initEnergy)

        start_time = time.time()

        #UPDATE FUNCTION
        for i in range(iter):
            #Memory point initialize
            memMgr.set_child_current(0)
            memMgr.set_current(0)

            #Update Barnes hut algorithm
            self.updateBarneshut(i, nc, expVar, memMgr, iter)

        end_time = time.time()
        print("Time = " + str(end_time - start_time))
        print("Current = " + str(memMgr.get_current())+"\t ChildCurrent = "+str(memMgr.get_child_current()))

        #Write graph information to file
        fr.writeFile(fileFullName, nc)


    
    def updateBarneshut(self, currentIter: int, p: nodeCollection, expVar : exponentVar, mgr: memoryManager, nrIteration: int):
        energySum = 0.0

        vect = p.getNodeVec()

        octTree = self.buildOctTree(p, mgr)

        self.adjustComponent(currentIter+1, nrIteration, expVar)

        attrExponent =  expVar.getAttrExponent()
        repuExponent = expVar.getRepuExponent()

        XY = [0.0] * const.DIM
        X1Y1 = [0.0] * const.DIM
        oldXY = [0.0] * const.DIM
        bestDir = [0.0] * const.DIM

        for i in range(len(vect)):

            for z in range(const.DIM):
                bestDir[z] = 0.0

            oldEnergy = p.getEnergy(vect[i], expVar, octTree)
            p.setDir(vect[i], bestDir, expVar, octTree)

            for k in range(const.DIM):
                X1Y1[k] = vect[i].getValue(k)
                XY[k] = X1Y1[k]
                oldXY[k] = X1Y1[k]

            bestEnergy = oldEnergy
            bestMultiple = 0

            for k in range(const.DIM):
                bestDir[k] = bestDir[k] / 32.0

            multiple = 32
            while multiple >= 1 and (bestMultiple == 0 or bestMultiple // 2 == multiple):
                octTree.removeNode(vect[i], XY, 0, mgr)
                for ss in range(const.DIM):
                    vect[i].setValue(oldXY[ss] + bestDir[ss] * multiple, ss)
                    XY[ss] = oldXY[ss] + bestDir[ss] * multiple

                octTree.addNode(vect[i], XY, 0, mgr)
                curEnergy = p.getEnergy(vect[i], expVar, octTree)

                if(curEnergy < bestEnergy):
                    bestEnergy = curEnergy
                    bestMultiple = multiple

                multiple //= 2

            multiple = 64
            while multiple <= 128 and bestMultiple == multiple//2:
                octTree.removeNode(vect[i], XY, 0, mgr)
                for ss in range(const.DIM):
                    vect[i].setValue(oldXY[ss] + bestDir[ss] * multiple, ss)
                    XY[ss] = oldXY[ss] + bestDir[ss] * multiple
                
                octTree.addNode(vect[i], XY, 0, mgr)
                curEnergy = p.getEnergy(vect[i], expVar, octTree)

                if(curEnergy < bestEnergy):
                    bestEnergy = curEnergy
                    bestMultiple = multiple

                multiple *= 2

            octTree.removeNode(vect[i], XY, 0, mgr)
            for ss in range(const.DIM):
                vect[i].setValue(oldXY[ss] + bestDir[ss] * bestMultiple, ss)
                XY[ss] = oldXY[ss] + bestDir[ss] * bestMultiple

            octTree.addNode(vect[i], XY, 0, mgr)
            energySum += bestEnergy

            print("#### ITER[" + str(currentIter + 1) + "]  E =" + str(energySum) + "  ATT =" + str(attrExponent) + "  REP =" + str(repuExponent))

            return True


    def currentDateTime():
        now = time.time()
        tstruct = time.localtime(now)
        formatted_time = time.strftime("%Y-%m-%d.%X", tstruct)
        return formatted_time

    def buildOctTree(self, ncp:nodeCollection, mgr:memoryManager) -> octTree:
        temp = [0.0] * const.DIM
        positionTemp = [0.0] * const.DIM
        minPos = [999999.0] * const.DIM
        position = [0.0] * const.DIM
        maxPos = [-999999.0] * const.DIM
        
        vect = ncp.getNodeVec()
        for s in range(len(vect)):
            if vect[s].getDegree() == 0:
                continue

            for z in range(const.DIM):
                position[z] = vect[s].getValue(z)
            
            for d in range(const.DIM):
                minPos[d] = min(position[d], minPos[d])
                maxPos[d] = max(position[d], maxPos[d])
    
        # provide additional space for moving nodes
        for d in range(const.DIM):
            posDiff = maxPos[d] - minPos[d]
            maxPos[d] += posDiff / 2
            minPos[d] -= posDiff / 2

        # add nodes with non-zero weight to the octtree
        result = mgr.get_Instance()
        result.setElement(None, temp, minPos, maxPos, mgr)

        for s in range(len(vect)):
            for kk in range(const.DIM):
                positionTemp[kk] = vect[s].getValue(kk)
            t = vect[s]
            result.addNode(t, positionTemp, 0, mgr)

        return result
    


    def adjustComponent(self, i: int, iter: int, expVar:exponentVar):
        if iter >= 50 and expVar.getFinalRepuExponent() < 1.0:
            expVar.setAttrExponent(expVar.getFinalAttrExponent())
            expVar.setRepuExponent(expVar.getFinalRepuExponent())

            if i < 0.6 * iter:
                expVar.setAttrExponent(expVar.getAttrExponent() + 1.1 * ( 1.0 - expVar.getFinalRepuExponent() ))
                expVar.setRepuExponent(expVar.getRepuExponent() + 0.9 * ( 1.0 - expVar.getFinalRepuExponent() ))
            elif i <= 0.9 * iter:
                factor = (0.9 - (float(i) / iter)) / 0.3
                expVar.setAttrExponent(expVar.getAttrExponent() + 1.1 * ( 1.0 - expVar.getFinalRepuExponent() ) * factor)
                expVar.setRepuExponent(expVar.getRepuExponent() + 0.9 * ( 1.0 - expVar.getFinalRepuExponent() ) * factor)