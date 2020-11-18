from random import randint
upperBound = 1000
res = lambda x=0: randint(x,upperBound)

with open("input.txt","w") as file:
    file.write("{} {}\n".format(res(),res()))
    package = res(1)
    shipper = res(1)
    while shipper >= package or shipper == 1:
        shipper =res(1)
    file.write("{} {}\n".format(package,shipper))
    for i in range(package):
        file.write(" ".join([str(res()) for i in range(4)]))
        file.write("\n")
