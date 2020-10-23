import copy

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

class Board:
    def __init__(self, _info):
        if type(_info) == type(self):
            self.size = _info.size
            self.queensCol = copy.deepcopy(_info.queensCol)
            self.bannedDiagonal={
                "back":[],
                "front":[]
            }
        else:
            try:
                self.size = int(_info)
            except Exception as err:
                pass
            self.queensCol = []
            self.bannedDiagonal = []
            
    def posCheck(self,row,col):
        if not col in self.queensCol:
            backDiagonal = row - col
            frontDiagonal = row + col +self.size
            if not (backDiagonal in self.bannedDiagonal or frontDiagonal in self.bannedDiagonal):
                return (backDiagonal,frontDiagonal)
        return None

    def put(self,col,diagonal=None):
            self.bannedDiagonal.extend(diagonal)
            self.queensCol.append(col)
            return self

    
    def isPerfect(self):
        return len(self.queensCol)==self.size
    
    def numQueens(self):
        return len(self.queensCol)

    def __repr__(self):
        n = self.size
        res =[["0"]*n for i in range(n)]
        row = 0
        for key in self.queensCol:
            res[row][key]= "1"
            row+=1
        return "\n".join([(" | ".join(k)) for k in res])+"\n"+str(self.bannedDiagonal)+"\n"+str(self.queensCol)

class Queue(Stack):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class DiagonalIndex():
    def __init__(self,n):
        backDiagonal = [[0 for i in range(n)] for i in range(n)]
        frontDiagonal = [[0 for i in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                backDiagonal[i][j]=i-j+n-1
                frontDiagonal[i][j]=i+j
        self.backDiagonal=backDiagonal
        self.frontDiagonal=frontDiagonal
        self.size = n
    def getDiagonal(self,row,cow):
        if row > self.size or cow > self.size:
            return "invalid index"
        else:
            return (self.backDiagonal[row][cow],self.frontDiagonal[row][cow])
if __name__ =="__main__":
    pass