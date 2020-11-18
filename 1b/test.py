# Them cac thu vien neu can
from functools import reduce
from random import randint,choice,random
from copy import deepcopy as dp
from math import e

location,amount,packages,shipperNum = None

def log(func):
    def inner(*args):
        string =lambda x : "|{:<25}|".format(x) if len(str(x)) < 16 else "|{:<25}|".format(str(x))
        # print(*[string(str(i)) for i in (func.__name__,*args)])
        return func(*args)
    return inner

def costCal(begin,package):
    return (
        5  +package[TSM.VOLUMNE] + package[TSM.WEIGHT]*2
        - (((begin[1]-package[1])**2 +(begin[2]-package[2])**2 )**(1/2))*1/2 
    ) - (10 if begin[0] == -1 else 0)

def readInput(self, file_input):
    with open(file_input,'r') as file:
        res = []
        line = file.readline()
        while line:
            temp = line.split(" ")
            res += [list(map( lambda x : int(x), temp))]
            line = file.readline()
        location = (-1,*res[0])
        amount,shipperNum  = res[1]
        packages = [[i] + ele for i,ele in enumerate(res[2:])]

def mapNode():
            self.Map = {}
            # self.Map = {f"-1-{i}": self.costCal((-1,*self.location),self.packages[i]) -10 for i in range(self.amount)}
            for i in range(-1,amount):
                for j in range(i+1,amount):
                    Map[f'{i}-{j}'] = (
                        costCal(packages[i] if not i == -1 
                        else location,packages[j])
                    )
            