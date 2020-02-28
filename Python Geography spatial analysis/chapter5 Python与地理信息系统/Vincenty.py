#Vincenty.py NAD83椭球体模型
import math
distance=None
x1=-90.212452861859035
y1=32.316272202663704
x2=-88.952170968942525
y2=30.4385599624660321
#椭球体参数
a=6378137#长半轴
f=1/298.257222101#逆扁平度
b=abs((f*a)-a)#短半轴
L=math.radians(x2-x1)
U1=math.atan((1-f)*math.tan(math.radians(y1)))
U2=math.atan((1-f)*math.tan(math.radians(y2)))
SinU1=math.sin(U1)
CosU1=math.cos(U1)
SinU2=math.sin(U2)
CosU2=math.cos(U2)
lam=L
for i in range(100):
    sinLam=math.sin(lam)
    cosLam=math.cos(lam)
    sinSigma=math.sqrt((CosU2*sinLam)**2+(CosU1*SinU2-SinU1*CosU2*cosLam)**2)
    if(sinSigma==0):
        distance=0#重合点
        break
    cosSigma=SinU1*SinU2+CosU1*CosU2*cosLam
    sigma=math.atan2(sinSigma,cosSigma)
    sinAlpha=CosU1*CosU2*sinLam/sinSigma
    cosSqAlpha=1-sinAlpha**2
    cos2SigmaM=cosSigma-2*SinU1*SinU2/cosSqAlpha

    if math.isnan(cos2SigmaM):
        cos2SigmaM=0#赤道线
    C=f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha))
    LP=lam
    lam=L+(1-C)*f*sinAlpha*(sigma+C*sinSigma*(cos2SigmaM+C*cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)))
    if not abs(lam-LP) > 1e-12:
        break
uSq=cosSqAlpha*(a**2-b**2)/b**2
A=1+uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq)))
B=uSq/1024*(256+uSq*(-128+uSq*(74-47*uSq)))
deltaSigma=B*sinSigma*(cos2SigmaM+B/4*(cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)-B/6*cos2SigmaM*(-3+4*sinSigma*sinSigma)*\
(-3+4*cos2SigmaM*cos2SigmaM)))
s=b*A*(sigma-deltaSigma)
distance=s
print(distance)