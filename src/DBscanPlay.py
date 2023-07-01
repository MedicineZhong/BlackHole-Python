import numpy as np
import constantly as const
import math
import Util
import time
from point import point


class DBscanPlay:

    def __init__(self) -> None:
        pass

    #@staticmethod
    def dbscanCalculator(self, inputFile: str, minPts: int, removePercentage: float):

        start_time = time.time()

        nodeNum = 0
        x = 0
        y = 0

        removeP = str(removePercentage * 100)

        with open(inputFile, 'r') as f:
            for line in f:
                if(line[0] == '#'):
                    continue
                else:
                    line = line.split('\t')
                    del1 = int(line[0])
                    x = int(line[0])
                    y = int(line[0])
                    nodeNum += 1

            f.close()


        #communitySelf = np.array(nodeNum)
        #points = np.zeros(nodeNum)
        points = np.zeros((const.DIM, nodeNum))
        
        visited = np.array([False] * nodeNum)
        countN = np.zeros(nodeNum)
        isSeed = np.array([False] * nodeNum)
        communityInfo = np.zeros(nodeNum)

        for ttt in range(nodeNum):
            for j in range(const.DIM):
                points[j][ttt] = 0

            visited[ttt] = False
            countN[ttt] = 0
            communityInfo[ttt] = -1
            isSeed[ttt] = False
        

        counter = 0

        with open(inputFile, 'r') as f:
            for line in f:
                if(line[0] == '#'):
                    continue
                else:
                    line = line.split('\t')
                    for j in range(const.DIM):
                        points[j][counter] = float(line[j])

                counter += 1
            f.close()

        dist_vec = np.zeros(nodeNum)
        dist_sorted = np.zeros(nodeNum)

        eps = 0.0

        for i in range(nodeNum):
            for j in range(nodeNum):
                dist_sorted[j] = self.calcDist(points, i, j)

            np.sort(dist_sorted)
            dist_vec[i] = dist_sorted[minPts - 1]

        #To select the eps value
        np.sort(dist_vec)

        #NORMALIZATION
        #Removing outlier to maximal value

        trunc = nodeNum * removePercentage
        tr = int(trunc)

        print("Truncated # = " + str(tr))

        for i in range(tr):
            dist_vec[tr] = 0

        np.sort(dist_vec)

        #Save to point array
        original = np.zeros(nodeNum)
        for i in range(nodeNum):
            original[i] = point(i, dist_vec[i])

        #find minVal, maxVal of Y

        maxVal = -1.0
        minVal = 999999.0

        for i in range(nodeNum):
            if(original[i].y >= maxVal):
                maxVal = original[i].y
            if(original[i].y <= minVal):
                minVal = original[i].y

        #min-max normalization

        for i in range(nodeNum):
            original[i].x = ((original[i].x - 0) / nodeNum) * 1
            original[i].y = (original[i].y - minVal) / (maxVal - minVal)

        #rotation
        for i in range(nodeNum):
            original[i].x = original[i].x * math.cos(-math.pi/4.0) + (original[i].y - 1.0 )* math.sin(-math.pi/4.0)
            original[i].y = -1.0 * original[i].x * math.sin(-math.pi/4.0) + (original[i].y - 1.0 ) * math.cos(-math.pi/4.0)

        minVal = 999999.0
        minValueIdx = -1
        for i in range(nodeNum):
            if(original[i].y <= minVal):
                minVal = original[i].y
                minValueIdx = i

        print("Approximated Value for DBSCAN = " + str(dist_vec[minValueIdx]))
        eps = dist_vec[minValueIdx]
        
        #Algorithm Start

        for i in range(0, nodeNum):
            for j in range(0, nodeNum):
                if(self.calcDist(points, i, j) <= eps):
                    countN[i] += 1

        currentCmty = 0
        icmty = 0
        setN = []

        for i in range(0, nodeNum):
            visited[i] = True

            setN.clear()

            if(countN[i] >= minPts):
                isSeed[i] = True

                if(communityInfo[i] == -1):
                    currentCmty += 1
                    communityInfo[i] = currentCmty

                icmty = communityInfo[i]

                for j in range(0, nodeNum):
                    if(i == j):
                        continue

                    if(self.calcDist(points, i, j) <= eps):
                        setN.append(j)
                        if(countN[j] >= minPts):
                            isSeed[j] = True

                setN.sort()
                while len(setN) > 0:
                    IterPos = iter(setN)

                    cur = next(IterPos)
                    setN.remove(cur)

                    if visited[cur] == False:
                        visited[cur] = True

                        for k in range(nodeNum):
                            if cur == k:
                                continue
                            
                            if self.calcDist(points, cur, k) <= eps:
                                setN.append(k)
                                if countN[k] >= minPts:
                                    isSeed[k] = True

                    if(communityInfo[cur] == -1 or communityInfo[cur] == 0):
                        communityInfo[cur] = icmty

                for j in range(0, nodeNum):
                    if(i == j):
                        continue

                    if(self.calcDist(points, i, j) <= eps):
                        if(visited[j] == False):
                            visited[j] = True
                            communityInfo[j] = communityInfo[i]

            else: #mark P as noise
                if(communityInfo[i] == -1):
                    communityInfo[i] = 0

        end_time = time.time()

        fileName = inputFile + "_MinPts_" + str(minPts) + "_RemovePercent_" + str(removeP) + "_EPS_" + str(eps) + ".dat"

        with open(fileName, 'w') as f:
            for i in range(0, nodeNum):
                f.write(str(i +1) + "\t" + str(communityInfo[i]) + "\t" + isSeed[i] +"\n")
            f.close()

        print("Time = " + str(end_time - start_time))
        print("######################################\nDBSCAN IS FINISHED!")


    
    #@staticmethod
    # def calcDist2(self, a, i:int, j:int) -> float:
    #     sum = 0
    #     for z in range(const.DIM):
    #         sum += (a[z][i] - a[z][j]) ** 2
    #     return math.sqrt(sum)
    
    def calcDist(self, a, i, j):
        column_i = a[:, i]  # 提取第 i 列
        column_j = a[:, j]  # 提取第 j 列
        diff_squared = np.square(column_i - column_j)
        sum_squared_diff = np.sum(diff_squared)
        return np.sqrt(sum_squared_diff)

        