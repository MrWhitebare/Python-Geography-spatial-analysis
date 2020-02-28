#Visualization 使用Python Image Library 让LIDAR支持可视化
import numpy
from PIL import Image,ImageDraw,ImageOps
import colorsys
source=r"D:\Program Files\Python学习文档\samples\lidar\lidar.asc"
target=r"D:\Program Files\Python学习文档\samples\lidar\Visualization.bmp"
array=numpy.loadtxt(source,skiprows=6)
'''
img=Image.fromarray(array).convert("RGB")
#图片增强，平衡和对比增强
img=ImageOps.equalize(img)
img=ImageOps.autocontrast(img)
img.save(target)
'''
#使用黑白模式以便在彩色图上叠加三个波段
img=Image.fromarray(array).convert('L')
#图片增强，平衡和对比增强
img=ImageOps.equalize(img)
img=ImageOps.autocontrast(img)
#开始构造渐变颜色板
palette=list()
#色调，饱和度，值
h=0.67
s=1
v=1
#渐变色带 蓝-绿-黄-橙-红
#蓝色=低高程区域 红色=高程较高区域
step=h/256
#构建调色板
for i in range(256):
    rp,gp,bp=colorsys.hsv_to_rgb(h,s,v)
    r=int(rp*255)
    g=int(gp*255)
    b=int(gp*255)
    palette.extend([r,g,b])
    h-=step
img.putpalette(palette)
img.save(target)
print("输出可视化图片！")
