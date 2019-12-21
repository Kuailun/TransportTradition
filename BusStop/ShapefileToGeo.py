import shapefile
from json import dumps
import xlwt

# 读入SHP数据
reader = shapefile.Reader("DataBus/bus_stops.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
   atr = dict(zip(field_names, sr.record))
   geom = sr.shape.__geo_interface__
   buffer.append(dict(type="Feature", \
    geometry=geom, properties=atr))



idList=[]
GPSList=[]

# 复制所有信息到GPS
for i in range(len(buffer)):
    GPSList.append(buffer[i])
    pass

# 仅保留每个线路的第一条
# sequency=0
# flag=True
# for i in range(len(buffer)):
#     seq=int(buffer[i]['properties']['sequence'])
#     if buffer[i]['properties']['layer'] in idList:
#         if(seq>sequency and flag):
#             GPSList.append(buffer[i])
#             sequency=seq
#         else:
#             flag=False
#         continue
#     else:
#         idList.append(buffer[i]['properties']['layer'])
#         sequency=seq
#         GPSList.append(buffer[i])
#         flag=True
#         pass
#     pass

# 删除重复的站
# idList=[]
# i=len(GPSList)-1
# while(i>=0):
#     if(GPSList[i]['properties']['id'] in idList):
#         del GPSList[i]
#     else:
#         idList.append(GPSList[i]['properties']['id'])
#         pass
#     i=i-1
#     pass
#
# i=len(GPSList)-1
# while(i>=0):
#     if(GPSList[i]['geometry']['coordinates'][0]<113.529465 or GPSList[i]['geometry']['coordinates'][0] > 113.783699):
#         del GPSList[i]
#     elif(GPSList[i]['geometry']['coordinates'][1]<34.698086 or GPSList[i]['geometry']['coordinates'][1] > 34.813889):
#         del GPSList[i]
#         pass
#     i=i-1
#     pass


workbook=xlwt.Workbook(encoding='utf-8')
worksheet=workbook.add_sheet('Data')

worksheet.write(0,1,"经度")
worksheet.write(0, 2, "纬度")
worksheet.write(0, 3, "层")
worksheet.write(0, 4, "序列")

for i in range(len(GPSList)):
    worksheet.write(i+1,1,GPSList[i]['geometry']['coordinates'][0])
    worksheet.write(i + 1, 2, GPSList[i]['geometry']['coordinates'][1])
    worksheet.write(i + 1, 3, GPSList[i]['properties']['layer'])
    worksheet.write(i + 1, 4, GPSList[i]['properties']['sequence'])
    worksheet.write(i+1,5,GPSList[i]['properties']['id'])
    pass
workbook.save('data.xls')
# geojson = open("pyshp-demo.json", "w")
# geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
# geojson.close()