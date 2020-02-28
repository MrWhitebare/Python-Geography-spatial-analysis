# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:33:17 2020

@author: 立文
"""
#StreetNet.py 街道路网规划
import networkx as nx
import math
from itertools import tee
import shapefile
import os
import time
def haversine(n0,n1):
    #计算连通图上的节点之间的阻抗值，找出和路径起始点和终点距离最短的节点
    x1,y1=n0
    x2,y2=n1
    x_dist=math.radians(x1-x2)
    y_dist=math.radians(y1-y2)
    y1_rad=math.radians(y1)
    y2_rad=math.radians(y2)
    a=math.sin(y_dist/2)**2+math.sin(x_dist/2)**2*math.cos(y1_rad)*math.cos(y2_rad)
    c=2*math.asin(math.sqrt(a))
    distance=c*6731
    return distance
def pairwise(iterable):
    #返回可迭代访问的二值元组
    a,b=tee(iterable)
    next(b,None)
    return zip(a,b)
s1=time.perf_counter()
shp=r"D:\Program Files\Python学习文档\samples\routing\road_network.shp"
#创建连通图并根据Shp文件中数据构造图中的边
G=nx.DiGraph()
r=shapefile.Reader(shp)
for s in r.shapes():
    for p1,p2 in pairwise(s.points):
        G.add_edge(tuple(p1),tuple(p2))
sg=list(nx.connected_component_subgraphs(G.to_undirected()))[0]#提取联通部件作为子连通图
r=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\routing\start_end.shp")
start=r.shape(0).points[0]
end=r.shape(1).points[0]
#遍历整个连通图为每条边声明距离值
for n0, n1 in sg.edges():
    dist = haversine(n0, n1)
    sg[n0][n1]["dist"] = dist
#遍历连通图上的节点寻找最短路径
nn_start=None
nn_end=None
start_delta=float("inf")
end_delta=float("inf")
for n in sg.nodes():
    s_dist=haversine(start,n)
    e_dist=haversine(end,n)
    if s_dist<start_delta:
        nn_start=n
        start_delta=s_dist
    if e_dist<end_delta:
        nn_end=n
        end_delta=e_dist
path=nx.shortest_path(sg,source=nn_start,target=nn_end,weight="dist")
target=r"D:\Program Files\Python学习文档\samples\routing\path.shp"
if os.path.exists(target):
    os.remove(target)
w=shapefile.Writer(target,shapefile.POLYLINE)
w.field("NAME","C",40)
w.line([[list(p) for p in path]])
w.record("route")
r.close()
w.close()
e=time.perf_counter()-s1
print("程序运行时间",e)