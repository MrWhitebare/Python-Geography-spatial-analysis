#AnalysisPath.py 最佳路径分析
import numpy
def astar(start,end,h,g):
    close_set=set()
    open_set=set()
    path=set()
    open_set.add(start)
    while open_set:
        cur=open_set.pop()
        if cur==end:
            return path
        close_set.add(cur)
        path.add(cur)
        options=[]
        y1=cur[0]
        x1=cur[1]
        if y1>0:#North
            options.append((y1-1,x1))
        if y1<h.shape[0]-1:#South 5-1
            options.append((y1+1,x1))
        if x1>0:#west
            options.append((y1,x1-1))
        if x1<h.shape[1]-1:#east 5-1
            options.append((y1,x1+1))
        if end in options:
            return path
        best=options[0]
        close_set.add(options[0])
        for i in range(1,len(options)):
            option=options[i]
            if option in close_set:
                continue
            elif h[option] <= h[best]:
                best=option
            elif g[option] <g[best]:
                best=option
                close_set.add(option)
            else:
                close_set.add(option)
        print(best,",",h[best],',',g[best])
        open_set.add(best)
    return []
#建立测试网格
width=5
height=5
start=(height-1,0)#网格左下角起始位置 数组
dx=width-1#网格右上角终点位置
dy=0
#空白网格
blank=numpy.zeros((width,height))
#距离网格
dist=numpy.zeros(blank.shape,dtype=numpy.int8)
#计算所有单元格的权重
for y,x in numpy.ndindex(blank.shape):
    dist[y][x]=abs((dx-x)+(dy-y))
cost=numpy.random.randint(1,16,(width,height))+dist
print("COST GRID (Value + Distance)")
print(cost)
print("DISTANCE　GRID ")
print(dist)
print("(Y,X), HEURISTIC ,DISTANCE")
#查找路径
path=astar(start,(dy,dx),cost,dist)
#创建和输出路径网格
path_grid=numpy.zeros(cost.shape,dtype=numpy.uint8)
for y,x in path:
    path_grid[y][x]=1
path_grid[dy][dx]=1
print("PATH GRID: 1=path")
print(path_grid)