#grid search
import sys,os
from random import random,choice
from copy import deepcopy
from time import time
from math import e
class Stack():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class Queue(Stack):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class State:
    def __init__(self,n):
        self.queens = [i for i in range(n)]
        State.size = n
        temp = lambda x:  [State.randomIndex() for i in range(x)]
        changes = temp(n)
        for i,key in enumerate(temp(n)):
            self.switch(key,changes[i],init = True)
        diagonal ={}
        for row,col in enumerate(self.queens):
            back,front = row-col-n,row+col
            if not diagonal.get(back): diagonal[back] = 1
            else: diagonal[back]+=1
            if not diagonal.get(front): diagonal[front] = 1
            else: diagonal[front]+=1        
        self.diagonal = diagonal

    def switch(self,*args,init = False):
        if not init:
            for i in args:
                self.diagonal[i-self.queens[i]-State.size]-= 1
                self.diagonal[ i+self.queens[i]] -= 1
        self.queens[args[0]],self.queens[args[1]]=self.queens[args[1]],self.queens[args[0]]
        if not init:
            for i in args:
                diagonal = (i-self.queens[i]-State.size,i+self.queens[i])
                for j in diagonal:
                    if self.diagonal.get(j):
                        self.diagonal[j]+=1
                    else :self.diagonal[j]=1
    @classmethod
    def randomIndex(cls,size = None):
        if not size: size = cls.size
        return int((random()*(size))%size)
        
    def fitness(self):
        res = 0
        for key in self.diagonal.values():
            if key > 1:
                res += ((key-1)*key)//2
        return -res

    def __eq__(self,other):
        return self.queens == other.queens

    def __repr__(self):
        return str(self.queens) #+ '\n'+ str(list(self.diagonal.values()))
    
    @staticmethod
    def simpleFiness(lst):
        for i,j in enumerate(lst):
            if i != State.size-1:
                for x,y in enumerate(lst[i+1:]):
                    if abs(x+1) == abs(j - y): return False
        return True
    

    def blindSolve(self,frontier):

        lst = self.queens.copy()
        frontier = frontier
        frontier.add([lst,0])  
        count = 0       
        while not frontier.empty():
            cur = frontier.remove()
            if State.simpleFiness(cur) == True: return cur
            count+= 1
            #print(cur,count)
            row = cur[1]
            if row != State.size-1:
                for j in range(State.size-1,row,-1):
                    temp = deepcopy(cur)
                    #temp.switch(row,j+row)
                    temp[0][row],temp[0][j] =temp[0][j],temp[0][row] 
                    temp[1] +=1
                    frontier.add(temp)

def solve(n):
    T = 1000
    alpha = 0.89
    cur = State(n)
    while True:
        c = n *(5)
        T0 = T
        count = 0
        cur  = cur
        current = cur.fitness()
        while True:
            i = State.randomIndex()
            j = State.randomIndex()
            while j == i: j = State.randomIndex()
            temp = deepcopy(cur)
            temp.switch(i,j)
            tempFitness = temp.fitness()
            change = False
            if tempFitness == 0: return temp
            if tempFitness>current:
                cur,current = temp,tempFitness
                #print('change better')
            else:
                p = random()
                if p < e **((tempFitness-current)/(T0)):
                    cur,current,change = temp,tempFitness,True
                    #print('change worst')
            T0 = alpha*T0
            #print(current,'   |   ',i,j,'   |   ',count,'   |   ',change)
         
            count+=1
            

def main():

    print(solve(500))



start_time = time()
main()
print("--- %s seconds ---" % (time() - start_time))