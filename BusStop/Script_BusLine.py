import requests
from pyquery import PyQuery as pq
import json

def generateStation(content):
    if not content.status_code == 200:
        print('ID列表返回值错误，错误代码:', content.status_code)
        return None

    # 转换编码方式
    content = str(content.content, encoding='utf8')
    html = pq(content)
    txt = html('#scrollTr')

    stations=txt.children()
    r_data=[]
    i=0
    for item in stations:
        item = pq(item)
        item = item('a')
        item = pq(item)
        name=item('em').text()
        r_data.append({'index':i,'name':name})
        i=i+1
        pass
    return r_data

def generateData(content):
    if not content.status_code == 200:
        print('ID列表返回值错误，错误代码:', content.status_code)
        return None

    # 转换编码方式
    content=str(content.content,encoding='utf8')
    html=pq(content)
    txt=html('.ChinaTxt')

    # 提取巴士线路信息
    r_data=[]
    for item in txt:
        item=pq(item)
        item=item('dd')
        items=item.children()
        for line in items:
            line=pq(line)
            r_data.append({'url':line.attr('href'),'title':line.attr('title')})
            pass
        pass
    return r_data
    pass
if __name__ == "__main__":
    url="https://bus.mapbar.com/zhengzhou/xianlu/"

    response = requests.get(url=url)
    busLine=generateData(response)

    result=[]
    for i in range(len(busLine)):
        url=busLine[i]['url']
        response = requests.get(url=url)
        busStations=generateStation(response)
        result.append({"name":busLine[i]['title'],'data':busStations})
        print(busLine[i]['title'])
        pass

    with open('busStops.json','w',encoding='utf-8') as f:
        json.dump(result,f)

    pass