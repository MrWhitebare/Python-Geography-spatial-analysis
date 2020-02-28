#Flood_fill.py
import numpy
from linecache import getline
import time
def floodFill(c,r,mask):
    '''
    从起始点(c=column,r=row-a.k x,y)
    开始遍历只包含0和1的掩模数组
    然后返回和起始单元格相连值为1的数组
    '''
    filled=set()#已填充单元格
    fill=set()#待填充单元格
    fill.add((c,r))
    width=mask.shape[1]-1
    heigth=mask.shape[0]-1
    #输出淹没数组
    flood=numpy.zeros_like(mask,dtype=numpy.int8)
    #遍历和修改需要检查的单元格，当填充时获取一个单元格
    while fill:
        x,y=fill.pop()
        if y==heigth or x==width or x<0 or y<0:
            continue
        if mask[y][x]==1:
            flood[y][x]=1
            filled.add((x,y))
            #检查相邻单元格
            west=(x-1,y)
            east=(x+1,y)
            north=(x,y-1)
            south=(x,y+1)
            if west not in filled:
                fill.add(west)
            if east not in filled:
                fill.add(east)
            if north not in filled:
                fill.add(north)
            if south not in filled:
                fill.add(south)
    return flood
start=time.perf_counter()
source=r"D:\Program Files\Python学习文档\samples\FloodFill\terrain.asc"
target=r"D:\Program Files\Python学习文档\samples\FloodFill\flood90.asc"
print("Open image...")
img=numpy.loadtxt(source,skiprows=6)
print("Image Open")
#掩模高程低于70m的区域
wet=numpy.where(img<90,1,0)
print("Image masked")
#使用内置linecache循环解析头部信息
hdr=[getline(source,i) for i in range(1,7)]
values=[float(h.split(" ")[-1].strip()) for h in hdr]
cols,rows,lx,ly,cell,nd=values
xres=cell
yres=cell*-1
#屏幕坐标中洪水的起始点
sx=2582
sy=2057
print("Beginning flood fill")
fid=floodFill(sx,sy,wet)      
header=""
for i in range(6):
    header+=hdr[i]
print("Saving grid")
#打开输出文件，添加hdr值
with open(target,"wb") as f:
    f.write(bytes(header,'UTF-8'))
    numpy.savetxt(f,fid,fmt="%1i")
end=time.perf_counter()-start
print("洪水掩模模型运行时间",end)