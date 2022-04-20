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


def mini(explore,distance):
    minimum=float("inf")#initialize the minimun be infinite that any value can be relpaced in varaible minimum at first
    index=0#use to record the minimum's index
    for i in range(len(explore)):#travel whole explore[]
        if distance[explore[i]]<minimum:
            minimum=distance[explore[i]]
            index=i
    return index



def ucs(start, end):
    # Begin your code (Part 3)
    num_visited=0
    Prev=defaultdict(str)
    explore=[]
    distance=defaultdict(float)
    explore.append(start)
    distance[start]=0
    visit[str(start)]=1
    while len(explore)!=0:
        index=mini(explore,distance)#every round choose the minimum index one to visited
        Start=str(explore.pop(index))#after visited, pop it
        visit[Start]=1
        num_visited+=1
        if Start==str(end):#ensure that if the visit node is end node, then stop the program
            dist=distance[str(end)]#distance will always record the shortest distance for each node
            explore.clear()
            break
        for i in range(len(dict[Start])):
            End=dict[Start][i][0]
            if visit[End]!=1:
                if End not in explore:#if the node had already in the queue, don't append it again
                    explore.append(End)
                if End in distance:
                    if distance[End]>distance[Start]+float(dict[Start][i][1]):
                        distance[End]=distance[Start]+float(dict[Start][i][1])#updata the shortest distance
                        Prev[End]=Start
                else:
                    Prev[End]=Start
                    distance[End]=distance[Start]+float(dict[Start][i][1])
        distance[index]=float("inf")#To avoid the distance keep be compared by the mini function, after visited, assign infinite to the distance
        
    path=[]
    path.append(str(end))
    while path[0]!=str(start):
        path.insert(0,Prev[path[0]])
    for i in range(len(path)):
        path[i]=int(path[i])
    return path, dist, num_visited 
    raise NotImplementedError("To be implemented")
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
