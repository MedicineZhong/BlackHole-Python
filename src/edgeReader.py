from nodeCollection import nodeCollection
from blackHoleNode import node as blackHoleNode
import constantly as const

class edgeReader:

    def readFile(self, filePath: str, ncp: nodeCollection):
        maxValue = 0
        with open(filePath, 'r') as f:
            
            for line in f:
                if(line[0] == '#'):
                    continue
                else:
                    line = line.split('\t')
                    id1 = int(line[0])
                    id2 = int(line[1])
                    if(id1 > id2):
                        if(id1 > maxValue):
                            maxValue = id1
                    else:
                        if(id2 > maxValue):
                            maxValue = id2

        ncp.setDegMat(maxValue)
            
        with open(filePath, 'r') as f:
            for line in f:
                if(line[0] == '#'):
                    continue
                else:
                    line = line.split('\t')
                    id1 = int(line[0])
                    id2 = int(line[1])
                    ncp.putNode(id1, id2)
                    ncp.putNode(id2, id1)


    def writeFile(self, filePath: str, ncp: nodeCollection):
        with open(filePath, 'w') as f:
            for i in range(len(ncp.nodeVec)):
                node = ncp.nodeVec[i]
                f.write(str(node.getID()) + "\t")
                for j in range(const.DIM):
                    f.write(str(node.getValue(j)) + "\t")

                f.write("\n")
