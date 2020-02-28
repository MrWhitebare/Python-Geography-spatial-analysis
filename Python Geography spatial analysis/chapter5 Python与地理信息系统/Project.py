#Project.py
import utm
Y=479747.0453210057
X=5377685.825323031
zone=32
band='U'
print(utm.to_latlon(Y,X,zone,band))#UTM投影转化地理坐标
