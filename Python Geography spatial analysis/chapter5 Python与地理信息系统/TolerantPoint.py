#TolerantPoint.py 点包容性公式
def point_in_poly(x,y,poly):
    #判断点是否是顶点
    if (x,y) in poly:
        return True
    #判断点是否在边框上
    for i in range(len(poly)):
        p1=None
        p2=None
        if i==0:
            p1=poly[0]
            p2=poly[1]
        else:
            p1=poly[i-1]
            p2=poly[i]
        if p1[1]==p2[1] and p1[1] ==y and x > min(p1[0],p2[0]) and x < max(p1[0],p2[0]):
            return True
    n=len(poly)
    inside=False

    p1x,p1y=poly[0]
    for i in range(n+1):
        p2x,p2y=poly[i%n]
        if y>min(p1y,p2y):
            if y<=max(p1x,p2x):
                if x<=max(p1x,p2x):
                    if p1y !=p2y:
                        xints=(y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x ==p2x or x<=xints:
                        inside=not inside
        p1x,p1y=p2x,p2y
    if inside:
        return True
    else:
        return False
#判断一个点是否包含在某区域
myPolygon=[(-70.593016,-33.416032),(-70.589604,-33.415370),(-70.589046,-33.417340),(-70.592351,-33.417949),(-70.593016,-33.416032)]
#测试点坐标
lon=-70.593016#-70.592000
lat=-33.416032#-33.416000
print(point_in_poly(lon,lat,myPolygon))
#测试该点是否在国境线上
lon=-70.593016
lat=-33.416032
print(point_in_poly(lon,lat,myPolygon))