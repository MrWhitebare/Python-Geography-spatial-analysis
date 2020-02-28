#PNGCanvasShapefile.py 使用PNGCancvs库创建照片
import shapefile
import pngcanvas
reader=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\hancock\hancock.shp")
xdist=reader.bbox[2]-reader.bbox[0]#bbox[0] xmin bbox[1] ymin bbox[2] xmax bbox[3] ymax
ydist=reader.bbox[3]-reader.bbox[1]
iwidth=400
iheight=600
xratio=iwidth/xdist
yratio=iheight/ydist
pixels=list()
for x,y in reader.shapes()[0].points:
    px=int(iwidth-((reader.bbox[2]-x)*xratio))
    py=int((reader.bbox[3]-y)*yratio)
    pixels.append([px,py])
canvas=pngcanvas.PNGCanvas(iwidth,iheight)
canvas.polyline(pixels)
pngfile=open(r"D:\Program Files\Python学习文档\samples\hancock_pngcancvs.png","wb")
pngfile.write(canvas.dump())
pngfile.close()
print("创建照片完成！")

