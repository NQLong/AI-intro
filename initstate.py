from random import random, choice
def init(n):
    lst = [i for i in range(n)]
    queens = [-1] * n
    dp = [0]* (2*n - 1)
    dm = [0]* (2*n - 1)
    for i in range(2*n):
        col = choice(lst)
        for j in range(10):
            row = choice(range(n))
            if queens[row] != -1:
                plus, minus = row + col, row - col + n - 1
                if dp[plus] ==0 and dm[minus] == 0:
                    dp[plus] , dm[minus] = 1,1
                    queens[row] = col
                    lst.remove(col)
    for row,col in enumerate(queens):
        if col < 0:
            col = choice(lst)
            lst.remove(col)
            queens[row] = col
            plus, minus = row + col, row - col + n - 1
            dp[plus] += 1
            dm[minus] +=1
    return (queens,dp,dm)


print(init(10))




#plus, minus = row + col, row - col + len(queens) - 1