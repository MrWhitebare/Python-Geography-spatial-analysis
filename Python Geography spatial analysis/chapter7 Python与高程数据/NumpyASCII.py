#NumpyASCII.py 使用Numpy读取grids，写入grids格式
import numpy
import linecache
myArray=numpy.loadtxt(r"D:\Program Files\Python学习文档\samples\myGrid.asc",skiprows=6)
header="ncols {}\n".format(myArray.shape[1])#列
header+="nrows {}\n".format(myArray.shape[0])#行
header+="xllcorner 277750.0\n"
header+="yllcorner 6122250.0\n"
header+="cellsize 1.0\n"
header+="NODATA_value -9999"
numpy.savetxt(r"D:\Program Files\Python学习文档\samples\myArray.asc",myArray,header=header,fmt="%1.2f")
with open("myArray.asc","w") as file:
    file.write(header)
    numpy.savetxt(file,myArray,fmt="%1.2f")
    file.close()
