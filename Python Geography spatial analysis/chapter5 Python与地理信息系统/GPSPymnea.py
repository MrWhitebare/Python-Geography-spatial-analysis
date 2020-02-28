# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 22:15:05 2020

@author: 立文
"""
#GPSPymnea.py 使用GPS数据
from pynmea2.stream import NMEAStreamReader
'''
nmea_file = pynmea2.NMEAFile(r"D:\Program Files\Python学习文档\samples\GPS\nmea.txt")
print(nmea_file.readline())
records = []
with pynmea2.NMEAFile(r"D:\Program Files\Python学习文档\samples\GPS\nmea.txt") as nmea_file:
    for record in nmea_file:
        records.append(record)
print('Count of records:', len(records))
print('The last record:', repr(records[-1]))
input_stream=r"D:\Program Files\Python学习文档\samples\GPS\nmea.txt"
streamreader = NMEAStreamReader(input_stream)
'''
nmeaFile=open(r"D:\Program Files\Python学习文档\samples\GPS\nmea.txt")
nmea_stream=NMEAStreamReader(stream=nmeaFile)
next_data=nmea_stream.next()
nmea_object=list()
while next_data:
    nmea_object+=next_data
    next_data=nmea_stream
#解析NMEA流
for nmea_ob in nmea_object:
    if hasattr(nmea_ob,"lat"):
        print("Lat/Lon:(%s ,%s)"% (nmea_ob.lat,nmea_ob.lon))