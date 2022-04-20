import csv
from collections import defaultdict

file=open('edges.csv')
dict=defaultdict(list)
visit=defaultdict(str)
lines=file.readlines()

for line in lines:
    queue=[]
    data=line.split(',')
    queue.append(data[1])#end
    queue.append(data[2])#distance
    queue.append(data[3].replace("\n",""))#speed limit
    dict[data[0]].append(queue)
    visit[data[0]]=0


def dfs(start, end):
    # Begin your code (Part 2)
    num_visited=0
    Prev=defaultdict(str)
    explore=[]
    explore.append(start)
    visit[str(start)]=1
    while len(explore)!=0:
        Start=str(explore.pop())#FILO so pop from the tail of the stack
        for i in range(len(dict[Start])):
            End=dict[Start][i][0]
            if visit[End]!=1:
                num_visited+=1
                visit[str(End)]=1
                Prev[End]=Start
                explore.append(End)
                if End==str(end):
                    explore.clear()
                    break
    path=[]
    dist=0
    path.append(str(end))
    while path[0]!=str(start):
        for i in range(len(dict[Prev[path[0]]])):
            if dict[Prev[path[0]]][i][0]==path[0]:
                dist+=float(dict[Prev[path[0]]][i][1])
        path.insert(0,Prev[path[0]])
    for i in range(len(path)):
        path[i]=int(path[i])
    return path, dist, num_visited 
    raise NotImplementedError("To be implemented")
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
