# Them cac thu vien neu can
from functools import reduce
from random import randint,choice,random
from copy import deepcopy as dp
from math import e

def log(func):
    def inner(*args):
        string =lambda x : "|{:<25}|".format(x) if len(str(x)) < 16 else "|{:<25}|".format(str(x))
        # print(*[string(str(i)) for i in (func.__name__,*args)])
        return func(*args)
    return inner

def assign(file_input, file_output):
    
    

    class TSM:
        file_input : str
        file_output: str

        WEIGHT = 4
        VOLUMNE = 3
        def __repr__(self):
            return TSM.__name__
        def __init__(self,file_input, file_output):
            self.readInput(file_input)
            self.mapNode()
        @log
        def readInput(self, file_input):
            with open(file_input,'r') as file:
                res = []
                line = file.readline()
                while line:
                    temp = line.split(" ")
                    res += [list(map( lambda x : int(x), temp))]
                    line = file.readline()
                # res = list(map( lambda x : int(x), res))
                
                self.location = res[0]
                self.amount,self.shipperNum  = res[1]
                self.packages = [[i] + ele for i,ele in enumerate(res[2:])]
                  
        @staticmethod
        def costCal(begin,package):
            return (
                5  +package[TSM.VOLUMNE] + package[TSM.WEIGHT]*2
                - (((begin[1]-package[1])**2 +(begin[2]-package[2])**2 )**(1/2))*1/2 
            ) - (10 if begin[0] == -1 else 0)
        
        @log
        def mapNode(self):
            self.Map = {}
            # self.Map = {f"-1-{i}": self.costCal((-1,*self.location),self.packages[i]) -10 for i in range(self.amount)}
            for i in range(-1,self.amount):
                for j in range(i+1,self.amount):
                    self.Map[f'{i}-{j}'] = self.costCal(self.packages[i] if not i == -1 else (-1,*self.location),self.packages[j])
            # print(self.Map)
        @log
        def assignPackage(self,shiperNo,package,packageCost,shipper=None,cost=None,position=None):
            if not shipper: shipper = self.shipper
            if not cost: cost = self.cost
            if not position: position = len(shipper[shiperNo])
            prev = front = 0
            if position == 0: prev,front = -1,shipper[shiperNo][0]
            elif position == len(shipper[shiperNo]): prev,front =shipper[shiperNo][-1],None
            else: prev,front =shipper[shiperNo][position-1],shipper[shiperNo][position]
            cost[shiperNo] += (
                self.getCost(prev,package)
                - ((self.getCost(prev,front)+self.getCost(package,front)) if front else 0)
            )
            shipper[shiperNo].insert(position,package)
            # cost[shiperNo] += packageCost
        
        @log
        def removePackage(self,shiperNo,package,shipper,cost,position):
            prev = -1 if position ==0 else shipper[shiperNo][position-1]
            front = None if position == len(shipper[shiperNo]) -1 else shipper[shiperNo][position+1]
            
            cost[shiperNo] += (
                -self.getCost(prev,package)
                + ((self.getCost(prev,front) - self.getCost(package,front)) if front else 0)
            )
            del(shipper[shiperNo][position])
            # shipper[shiperNo].remove(package)
            
        @log
        def getCost(self,pac1,pac2):
            return self.Map[f'{pac1}-{pac2}'] if pac1<pac2 else self.Map[f'{pac2}-{pac1}']
        
        @log
        def initState(self):
            safe = [ i for i in range(self.amount)]
            shipper = [[] for i in range(self.shipperNum)]
            cost = [0]*self.shipperNum
            for i in range(self.shipperNum):
                package = choice(safe)
                safe.remove(package)
                shipper[i] += [package]
                cost[i] += self.Map[f'-1-{package}']
            while safe:
                package = choice(safe)
                safe.remove(package)
                minShip = cost.index(min(cost))
                latestMin = shipper[minShip][-1]
                costMin = self.getCost(latestMin,package)
                
                maxShip = cost.index(max(cost))
                latestMax = shipper[maxShip][-1]
                costMax = self.getCost(latestMax,package)

                if costMin < 0 and costMax < 0:
                    self.assignPackage(maxShip,package,costMax, shipper,cost)
                elif costMin > 0 and costMax > 0:
                    self.assignPackage(minShip,package,costMin, shipper,cost)
                elif costMin >0 and costMax <0:
                    if costMin >= abs(costMax):
                        self.assignPackage(minShip,package,costMin, shipper,cost)
                    else: self.assignPackage(maxShip,package,costMax, shipper,cost)
                else:
                    other = choice(range(self.shipperNum))
                    for i in range (5):
                        if not other in (minShip,maxShip): break
                        other = choice(range(self.shipperNum))
                    latestOther = shipper[other][-1]
                    otherCost = self.getCost(latestOther,package)
                    self.assignPackage(other,package,otherCost,shipper,cost)
                    
            print("done")
            return shipper,cost
        
        @log
        def fitness(self,shipper = None, cost = None):
            if not shipper: shipper = self.shipper
            if not cost: cost = self.cost

            res = 0
            for i in range(self.shipperNum):
                for j in range(i+1,self.shipperNum):
                    res += abs(cost[i] - cost[j])
            return res
        
        @log
        def solve(self):
            C1 = 40
            alpha = 0.99
            shipper, cost = self.initState()
            best = shipper
            bestFitness = self.fitness(shipper,cost)
            Timeout = 200000
            bestFitnessTimeout = Timeout
            while True:
                shipper, cost = self.initState()
                curFitness = self.fitness(shipper,cost)
                C2 = 10000
                T = 1000
                while C2 >= 0:
                    temp, tcost = dp(shipper),dp(cost)
                    tempFitness = curFitness
                    a = self.Heuristic(temp,tcost)
                    # print(a)
                    if a:
                        tempFitness = self.fitness(temp,tcost)
                        if tempFitness<curFitness:
                            shipper,cost,curFitness = temp,tcost,tempFitness
                            if curFitness< bestFitness: best,bestFitness,bestFitnessTimeout = dp(shipper),curFitness,Timeout

                        else:
                            p = random()
                            if p < e **(-(tempFitness-curFitness)/(T)):
                                print("worst")
                                shipper,cost,curFitness = temp,tcost,tempFitness
                    
                        T = alpha*T
                    if bestFitness == 0 or bestFitnessTimeout < 0: break    
                    bestFitnessTimeout -= 1
                    C2 -= 1
                if bestFitnessTimeout < 0: break
                C1-=1
            if C1 <= 1: print(C1) 
            print(best,bestFitness)
            file = open("res.txt","a")
            file.write(f"{bestFitness}\n")
                        
        @log   
        def Heuristic(self,shipper,cost):
            candidate = [0,0]
            if randint(0,99)>= 0:
                candidate = (cost.index(min(cost)),cost.index(max(cost)))
            else:
                candidate[0] = randint(0,self.shipperNum - 1)
                candidate[1] = randint(0,self.shipperNum - 1)
                while(candidate[0] == candidate[1]) : candidate[1] = randint(0,self.shipperNum - 1)
        
            
            picked = 0
            temp = (len(shipper[candidate[0]]) , len(shipper[candidate[1]]))
            # print(temp)
            if temp[0] ==1 and temp[1]== 1:
                return 0
            elif 1 in temp:
                if temp[0] == 1: picked = 1
            else:
                picked = randint(0,1)
            added = int(not bool(picked))
            # print((picked,added))
            
            before = abs(cost[candidate[0]] - cost[candidate[1]])

            packageIndex = randint(0,len(shipper[candidate[picked]])-1)
            package = shipper[candidate[picked]][packageIndex]
            packageDes = randint(0,len(shipper[candidate[added]]))
            
            self.removePackage(candidate[picked],package,shipper,cost,packageIndex)
            self.assignPackage(candidate[added],package,None,shipper,cost,packageDes)
            after = abs(cost[candidate[0]] - cost[candidate[1]])
            
            if after < before: return 1
            return -1
        @staticmethod
        def testresult(lst):
            cost = [0,0,0]
            for i,shipper in enumerate(lst):
                for i in range (-1,len(shipper)): pass
                    
    TSM(file_input,file_output).solve()


assign('input.txt', 'output.txt')

