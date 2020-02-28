#Vignette.py 创建彩色晕渲地形
from osgeo import gdal_array
from PIL import Image
import time
star=time.perf_counter()
relief=r"D:\Program Files\Python学习文档\samples\dem\relief.asc"
dem=r"D:\Program Files\Python学习文档\samples\dem\dem.asc"
target=r"D:\Program Files\Python学习文档\samples\dem\hillshade.tif"
background=gdal_array.numpy.loadtxt(relief,skiprows=6)#地形
foreground=gdal_array.numpy.loadtxt(dem,skiprows=6)[:-2, :-2]#DEM
#创建空白的3波段图片为DEM配色
rgb=gdal_array.numpy.zeros((3,len(foreground),len(foreground[0])),gdal_array.numpy.uint8)
#DEM类别高程区间上限值
classes=[356,649,942,1235,1528,1821,2114,2300,2700]
#颜色查找表
lut=[[63, 159, 152], [96, 235, 155], [100, 246, 174],
       [248, 251, 155], [246, 190, 39], [242, 155, 39],
       [165, 84, 26], [236, 119, 83], [203, 203, 203]]
start=1
for i in range(len(classes)):
    mask=gdal_array.numpy.logical_and(start<=foreground,foreground<=classes[i])
    for j in range(len(lut[i])):
        rgb[j]=gdal_array.numpy.choose(mask,(rgb[j],lut[i][j]))
    start=classes[i]+1
img1=Image.fromarray(background).convert('RGB')#地形阴影转化为PIL图片
img2=Image.fromarray(rgb.transpose(1,2,0)).convert('RGB')
hillshade=Image.blend(img1,img2,0.4)#使用40%透明度叠加2张图片
hillshade.save(target)
end=time.perf_counter()-star
print("程序运行时间",end)
