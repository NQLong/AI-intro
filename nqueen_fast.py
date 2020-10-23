import numpy as np
import time

start_time = time.time()
n = int(input("Enter n: "))

rs = np.zeros(n,dtype=np.int64)
board=np.zeros((n,n),dtype=np.int64)

k=0

if n%6==2 :

    for i in range(2,n+1,2) :
        #print i,
        rs[k]=i-1
        k+=1

    rs[k]=3-1
    k+=1
    rs[k]=1-1
    k+=1

    for i in range(7,n+1,2) :
        rs[k]=i-1
        k+=1

    rs[k]=5-1

elif n%6==3 :

    rs[k]=4-1
    k+=1

    for i in range(6,n+1,2) :
        rs[k]=i-1
        k+=1

    rs[k]=2-1
    k+=1

    for i in range(5,n+1,2) :

        rs[k]=i-1
        k+=1

    rs[k]=1-1
    k+=1
    rs[k]=3-1

else :

    for i in range(2,n+1,2) :

        rs[k]=i-1
        k+=1

    for i in range(1,n+1,2) :

        rs[k]=i-1
        k+=1

print("--- %s seconds ---" % (time.time() - start_time))

# for i in range(n) :
#     print("({},{})".format(i, rs[i]))

