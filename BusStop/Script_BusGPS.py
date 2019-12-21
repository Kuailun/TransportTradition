import json

data=json.load(open('busStops.json','r'))

cnt=0
for i in range(len(data)):
    cnt=cnt+len(data[i]['data'])
    pass
print(cnt)

name=[]
for i in range(len(data)):
    for j in range(len(data[i]['data'])):
        if data[i]['data'][j]['name'] in name:
            continue
        else:
            name.append(data[i]['data'][j]['name'])
        pass
    pass
print(len(name))