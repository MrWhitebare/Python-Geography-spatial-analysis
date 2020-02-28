#AnalysisDEM.py DEM数据最短路径分析
import numpy
import math
from linecache import getline
import time
def Euclid_distance(p1,p2):
    #根据两个点计算欧氏距离
    x1,y1=p1
    x2,y2=p2
    distance=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return int(distance)
def Weighted_score(cur,node,h,start,end):
    '''
    根据当前节点和邻接节点比较得出权重记录，基于Nisson绩点计算公式：f=g+h
    h代表“启发值”，指每个节点的高程值
    '''
    score=0
    cur_h=h[cur]#当前节点的高程值
    cur_g=Euclid_distance(cur,end)#当前节点与终点的距离
    cur_d=Euclid_distance(cur,start)#当前节点与起点的距离
    node_h=h[node]#相邻节点高程值
    node_g=Euclid_distance(node,end)#相邻节点与终点的距离
    node_d=Euclid_distance(node,start)#相邻节点与起点的距离
    #在向终点搜索的过程中比较给定地形的最高权重值
    if node_h<cur_h:
        score+=cur_h-node_h
    if node_g<cur_g:
        score+=10
    if node_d>cur_d:
        score+=10
    return score
def Astar(start,end,h):
    #A*搜索遍历网格的所有节点，记录每个节点的相邻节点，并将之与最佳记录匹配直到终点
    closed_set=set()#关闭节点集合
    open_set=set()#开始节点集合
    path=set()#输出路径集合
    open_set.add(start)#添加起始位置
    while open_set:
        cur=open_set.pop()#获取下一节点
        if cur==end:
            return path
        closed_set.add(cur)
        path.add(cur)
        options=[]#所有邻接节点
        y1=cur[0]
        x1=cur[1]
        if y1>0:#North
            options.append((y1-1,x1))
        if y1<h.shape[0]-1:#South
            options.append((y1+1,x1))
        if x1>0:#West
            options.append((y1,x1-1))
        if x1<h.shape[1]-1:#East
            options.append((y1,x1+1))
        if x1>0 and y1>0:#NorthWest
            options.append((y1-1,x1-1))
        if y1<h.shape[0]-1 and x1<h.shape[1]-1:#SouthEest
            options.append((y1+1,x1+1))
        if  y1<h.shape[0]-1 and x1>0:#SouthWest
            options.append((y1+1,x1-1))
        if y1>0 and  x1<h.shape[1]-1:#NorthEast
            options.append((y1-1,x1+1))
        if end in options:#如果邻接节点是终点，返回
            return path
        #存储最佳节点
        best=options[0]
        best_score=Weighted_score(cur,best,h,start,end)
        #处理其他7个节点方位
        for i in range(1,len(options)):
            option=options[i]
            if option in closed_set:
                continue
            else:#记录选项并和最佳节点比较
                option_score=Weighted_score(cur,option,h,start,end)
                if option_score>best_score:
                    best=option
                    best_score=option_score
                else:
                #如果节点不符合条件，将之归档
                    closed_set.add(option)
                print(best,Euclid_distance(best,end))
        open_set.add(best)
    return []
start=time.perf_counter()
source=r"D:\Program Files\Python学习文档\samples\LeastCostPath\dem.asc"#
target=r"D:\Program Files\Python学习文档\samples\LeastCostPath\path.asc"
print("Opening %s..." % source)
cost=numpy.loadtxt(source,skiprows=6)
print("Opened %s." % source)
#解析头部信息
hdr=[getline(source,i) for i in range(1,7)]
values=[float(ln.split(" ")[-1].strip()) for ln in hdr]
cols,rows,lx,ly,cell,nd=values
#起始位置
sx=1006
sy=954
#结束位置
dx=303
dy=109
print("Searching for path...")
p = Astar((sy, sx), (dy, dx), cost)
print("Path found.")
print("Creating path grid...")
path = numpy.zeros(cost.shape)
print("Plotting path...")
for y, x in p:
    path[y][x] = 1
path[dy][dx] = 1
print("Path plotted.")

print("Saving %s..." % target)
header = ""
for i in range(6):
    header += hdr[i]
# Open the output file, add the hdr, save the array
with open(target, "wb") as f:
    f.write(bytes(header, 'UTF-8'))
    numpy.savetxt(f, path, fmt="%4i")
end=time.perf_counter()-start
print("程序运行时间为:",end)
print("Done!")