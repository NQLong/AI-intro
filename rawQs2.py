from time import time
from random import random, choice
from functools import reduce
def  randomIndex(n):
    return int((random()*(n))%n)

def dinit(queens):
    n = len(queens)
    dp = [0] * (2*n -1)
    dm = dp.copy()
    for row, col in enumerate(queens):
        plus, minus = row + col, row - col + n - 1
        dp[plus] += 1
        dm[minus] += 1
    return (dp,dm)

def attackUpdate(queens,dp,dm):
    lst = []
    for row, col in enumerate(queens):
        plus, minus = row + col, row - col + len(queens) - 1
        if dp[plus] > 1 or dm[minus] > 1:
            lst.append(row)
    return lst

def solve(n):
        C1, C2 = 0.45, 32
        queens = [i for i in range(n)]
        lst = [0]*(2*n-1)
        while True:
            queens = queens.copy()
            for i in range(n):
                row = randomIndex(n)
                queens[i],queens[row] = queens[row], queens[i]
            dp, dm = dinit(queens)
            attacked = attackUpdate(queens,dp,dm)
            fitness = Fitness(dp,dm)
            limit = C1*fitness
            step = 0
            while step <= C2 * n:
                if fitness == 0: return queens
                for row in attacked:
                   other = choice(range(n))
                   if swapBetter(row,other,queens,dp,dm):
                        swap(row,other,queens,dp,dm)
                        fitness = Fitness(dp,dm)
                        if fitness < limit:
                            attacked = attackUpdate(queens,dp,dm)
                step += len(attacked)

def Fitness (dp,dm):
    cal = lambda x, y: x + (y - 1 if y != 0 else 0)
    return reduce(cal,dm,0) + reduce(cal,dp,0)
def swap(i,j,queens,dp,dm):
    n = len(queens)
    dp[i+queens[i]]     -=  1
    dm[i-queens[i]+n-1] -=  1
    dp[j+queens[j]]     -=  1
    dm[j-queens[j]+n-1] -=  1
    dp[i+queens[j]]     +=  1
    dm[i-queens[j]+n-1] +=  1
    dp[j+queens[i]]     +=  1
    dm[j-queens[i]+n-1] +=  1
    queens[i],queens[j]=queens[j],queens[i]

def swapBetter(i,j,queens,dp,dm):
    if i == j : return False
    n = len(queens)
    previous =  (   dp[i+queens[i]],
                    dm[i-queens[i]+n-1],
                    dp[j+queens[j]],
                    dm[j-queens[j]+n-1],
                    dp[i+queens[j]],
                    dm[i-queens[j]+n-1],
                    dp[j+queens[i]],
                    dm[j-queens[i]+n-1]
                )
    
    after =     (   dp[i+queens[i]] -1,
                    dm[i-queens[i]+n-1]-1,
                    dp[j+queens[j]] - 1,
                    dm[j-queens[j]+n-1] -1,
                    dp[i+queens[j]] + 1,
                    dm[i-queens[j]+n-1] + 1,
                    dp[j+queens[i]] + 1,
                    dm[j-queens[i]+n-1] +1
                )
    cal = lambda x, y: x + (y - 1 if y != 0 else 0)
    return reduce(cal,previous,0) > reduce(cal,after,0)


start_time = time()
file = open("log.txt",'w')
file.write(str(solve(50000)))
print("--- %s seconds ---" % (time() - start_time))
