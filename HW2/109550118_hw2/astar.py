import csv
from collections import defaultdict
from re import X

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

file2=open('heuristic.csv')
test1=defaultdict(float)#use test1 store the data to the end point(1079387396)
test2=defaultdict(float)#use test2 store the data to the end point(1737223506)
test3=defaultdict(float)#use test3 store the data to the end point(8513026827)
lines2=file2.readlines()
i=0
for line in lines2:
    if i==0:#avoid read the first line
        i+=1
        continue
    data=line.split(',')
    node=int(data[0])
    test1[node]=data[1]
    test2[node]=data[2]
    test3[node]=data[3].replace("\n","")

def mini(explore,cost):
    minimum=float("inf")
    index=0
    for i in range(len(explore)):
        if float(cost[explore[i]])<minimum:#in Astar case change to compare value in cost[]
            minimum=cost[explore[i]]
            index=i
    return index

def astar(start, end):
    # Begin your code (Part 4)
    if str(end)=='1079387396':
        test=test1
    if str(end)=='1737223506':
        test=test2
    if str(end)=='8513026827':
        test=test3
    #test represent data h(n)
    num_visited=0
    Prev=defaultdict(str)
    explore=[]
    distance=defaultdict(float)#g(n)
    cost=defaultdict(float)#store the value g(n)+h(n)
    explore.append(start)
    distance[start]=0
    cost[start]=test[start]#=0+h(start)
    visit[str(start)]=1
    while len(explore)!=0:
        index=mini(explore,cost)
        Start=str(explore.pop(index))
        visit[Start]=1
        num_visited+=1
        if Start==str(end):
            dist=cost[str(end)]
            explore.clear()
            break
        for i in range(len(dict[Start])):
            End=str(dict[Start][i][0])
            if visit[End]!=1:
                if End not in explore:
                    explore.append(End)
                if End in distance:
                    if distance[End]>distance[Start]+float(dict[Start][i][1]):
                        distance[End]=distance[Start]+float(dict[Start][i][1])#only distance need to update
                        Prev[End]=Start
                else:
                    Prev[End]=Start
                    distance[End]=distance[Start]+float(dict[Start][i][1])
            cost[End]=distance[End]+float(test[int(End)])#calculate the cost value by distance[]+test[]
        distance[index]=float("inf")#avoid to be compare later
        cost[index]=float("inf")#same as distance
    path=[]
    path.append(str(end))
    while path[0]!=str(start):
        path.insert(0,Prev[path[0]])
    for i in range(len(path)):
        path[i]=int(path[i])
    return path, dist, num_visited 
    raise NotImplementedError("To be implemented")
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
