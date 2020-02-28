# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:03:31 2020

@author: 立文
"""
from osgeo import gdal_array
import turtle
def histogram(a,bins=list(range(0,256))):
    fa=a.flat
    n=gdal_array.numpy.searchsorted(gdal_array.numpy.sort(fa),bins)
    n=gdal_array.numpy.concatenate([n,[len(fa)]])
    hist=n[1:]-n[:-1]
    return hist
def draw_histogram(hist,scale=True):
    turtle.setup(1000,600)
    turtle.color("black")
    #坐标轴
    axes=((-355,-200),(355,-200),(-355,-200),(-355,250))
    turtle.up()
    for p in axes:
        turtle.goto(p)
        turtle.down()
    turtle.up()
    turtle.goto(0,-250)
    #值
    turtle.write("Value",font=("Arial, ",12,"bold"))
    turtle.goto(-400,280)
    #频率
    turtle.write("Frequency",font=("Arial, ",12,"bold"))
    x=-355
    y=-200
    turtle.up()
    for i in range(1,11):
        x=x+65
        turtle.goto(x,y)
        turtle.down()
        turtle.goto(x,y-10)#坐标短线
        turtle.up()
        turtle.goto(x,y-25)
        turtle.write("{0}".format((i*25)),align="center")
    x=-355
    y=-200
    turtle.up()
    pixels=sum(hist[0])
    if scale:
        max=0
        for h in hist:
            hmax=h.max()
            if hmax >max:
                max=hmax
        pixels=max
    lable=int(pixels/10)
    for i in range(1,11):
        y=y+45
        turtle.goto(x,y)
        turtle.down()
        turtle.goto(x-10,y)
        turtle.up()
        turtle.goto(x-15,y-6)
        turtle.write("{0}".format((i*lable)),align="right")
    x_ratio=709.0/256
    y_ratio=450.0/pixels
    colors=["red","green","blue"]
    for j in range(len(hist)):
        h=hist[j]
        x=-354
        y=-199
        turtle.up()
        turtle.goto(x,y)
        turtle.down()
        turtle.color(colors[j])
        for i in range(256):
            x=i*x_ratio
            y=h[i]*y_ratio
            x=x-(709/2)
            y=y-199
            turtle.goto((x,y))
#src=r"D:\Program Files\Python学习文档\samples\FalseColor\Swap.tif"
#均衡化之后的图像
src=r"D:\Program Files\Python学习文档\samples\FalseColor\stretched.tif"
histograms=[]
array=gdal_array.LoadFile(src)
for b in array:
    histograms.append(histogram(b))
draw_histogram(histograms)
#draw_histogram(histograms,scale=False)    
turtle.pen(shown=False)
turtle.done()
        
        
        