# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 20:34:26 2020

@author: 立文
"""
import pymysql
connect=pymysql.connect(host='localhost',port=3306,user='root',passwd='admin',db='mysql')
#客户端：本地 端口号：3306 用户：root 密码：admin 数据库：mysql
cursor=connect.cursor()
cursor.execute("DROP DATABASE IF EXISTS spatial_db")#如果spatial_db存在，删除此数据库
cursor.execute("CREATE DATABASE spatial_db")#创建数据库spatial_db
cursor.close()
connect.close()
print("创建数据库spatial_db成功！")
connect=pymysql.connect(host='localhost',port=3306,user='root',passwd='admin',db='spatial_db')
cursor=connect.cursor()
cursor.execute("CREATE TABLE `spatial_db`.`PLACES` (`id` INT NOT NULL AUTO_INCREMENT,`Name` VARCHAR(50) NOT NULL,`location` GEOMETRY NOT NULL,PRIMARY KEY (`id`));")
cursor.execute("INSERT INTO `spatial_db`.`places`(`Name`,`location`) VALUES('New ORLEANS',st_GeomFromText('point(30.03 90.03)'));")
#point(x y)不用逗号分隔
cursor.execute("INSERT INTO `spatial_db`.`places`(`Name`,`location`) VALUES('MEMPHIS',st_geomfromtext('point(30.05 90.00)'));")
connect.commit()#提交创建内容
cursor.execute("SELECT st_AsText(location) FROM PLACES")
p1,p2=[p[0] for p in cursor.fetchall()]
cursor.execute("SET @p1=ST_GeomFromText('{}')".format(p1))
cursor.execute("SET @p2=ST_GeomFromText('{}')".format(p2))
cursor.execute("SELECT ST_Distance(@p1,@p2)")
d=float(cursor.fetchone()[0])
print("{:.2f} miles from New Orleans to Memphics".format(d*70))
#计算New Orleans 到达 Memphics 的距离。
cursor.close()
connect.close()