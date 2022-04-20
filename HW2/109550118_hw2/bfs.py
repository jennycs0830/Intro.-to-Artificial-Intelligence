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


def bfs(start, end):
    # Begin your code (Part 1)
    num_visited=0
    Prev=defaultdict(str)
    explore=[]#the FIFO queue record the node going to visit
    explore.append(start)#the first node to visit is the starting node
    visit[str(start)]=1#the node had been visited so assign visit[]=1
    while len(explore)!=0:#if the queue is not empty, then keep visiting the node in the queue
        Start=str(explore.pop(0))
        for i in range(len(dict[Start])):#do (# of subnode of Start) times
            End=dict[Start][i][0]
            if visit[End]!=1:#ensure that the node wouldn't be travel over one time
                num_visited+=1#calculate # of node had been traveled
                visit[str(End)]=1
                Prev[End]=Start
                explore.append(End)#push the End node into the queue that later will travel to
                if End==str(end):#if we found the End point then that the queue be empty to start the while loop
                    explore.clear()
                    break
    path=[]
    dist=0
    path.append(str(end))#because we used the Prev{} to record the previous node, so we start from the end point
    while path[0]!=str(start):#until we find the starting node
        for i in range(len(dict[Prev[path[0]]])):#find from the dict{} about the data if the edge
            if dict[Prev[path[0]]][i][0]==path[0]:#edge's end node
                dist+=float(dict[Prev[path[0]]][i][1])#claculate the total distance
        path.insert(0,Prev[path[0]])#update the path
    for i in range(len(path)):
        path[i]=int(path[i])
    return path, dist, num_visited 
    raise NotImplementedError("To be implemented")
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
