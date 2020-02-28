#Histogramblanced.py 直方图均衡化
from osgeo import gdal_array
import operator
from functools import reduce
def histogram(a,bins=list(range(0,256))):
    fa=a.flat
    n=gdal_array.numpy.searchsorted(gdal_array.numpy.sort(fa),bins)
    n=gdal_array.numpy.concatenate([n,[len(fa)]])
    hist=n[1:]-n[:-1]
    return hist
def stretch(a):
    #在gdal_array上传的图像数组中执行直方图均衡化操作
    hist=histogram(a)
    lut=[]
    for b in range(0,len(hist),256):
        #步长尺寸
        step=reduce(operator.add,hist[b:b+256])/256
        #创建均衡的查找表
        n=0
        for i in range(256):
            lut.append(n/step)
            n=n+hist[i+b]
    gdal_array.numpy.take(lut,a,out=a)
    return a
src=r"D:\Program Files\Python学习文档\samples\FalseColor\Swap.tif"
array=gdal_array.LoadFile(src)
stretched=stretch(array)
output=r"D:\Program Files\Python学习文档\samples\FalseColor\stretched.tif"
output=gdal_array.SaveArray(array,output,format="GTiff",prototype=src)
output=None
