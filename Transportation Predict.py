from geopy.distance import vincenty
import math
import numpy as np


def readData(p_path):

    # 读入数据
    table=[]
    try:
        with open(p_path,'rb') as f:
            for row in f:
                row = row.rstrip()
                row = row.decode("utf-8")
                row = row.split(',')
                if len(row) == 8:
                    table.append(row)
    except IOError:
        pass

    # 将数据转为float值
    index=[0,1,2,3,4,5]
    for i in range(len(table)):
        for j in range(len(index)):
            table[i][j]=float(table[i][j])
            pass
        pass
    return table

def filterData(p_data,p_speed,p_star):
    r_data=[]

    for i in range(len(p_data)):
        # 如果纬度不在范围内则删除
        if p_data[i][0]>90 or p_data[i][0]<-90:
            continue
        # 如果经度不在范围内则删除
        elif p_data[i][1]>180 or p_data[i][1]<-180:
            continue
        # 如果速度不在范围内则删除
        elif p_data[i][2]>p_speed or p_data[i][2]<0:
            continue
        # 如果卫星数量不在范围内则删除
        elif p_data[i][4]<p_star:
            continue
        # 如果时间戳有问题内则删除
        elif i<len(p_data)-1 and p_data[i][5]>=p_data[i+1][5]:
            continue
        r_data.append(p_data[i])
        pass
    return r_data

def segmentTripByTime(p_data,p_interval):
    i = 0
    currentTime = p_data[i][5]
    currentSegment = []
    Trips = []
    while i < len(p_data) - 1:
        if ((p_data[i + 1][5] - currentTime) * 24. * 3600 > p_interval):
            Trips.append(currentSegment)
            i = i + 1
            currentTime = p_data[i][5]
            currentSegment = []
            continue
            pass
        currentSegment.append(i)
        i = i + 1
        currentTime = p_data[i][5]
        pass
    Trips.append(currentSegment)

    i = len(Trips) - 1
    while (i >= 0):
        if (len(Trips[i]) < 10):
            del Trips[i]
            pass
        i = i - 1

    subTrip = []
    mTrip = []
    for i in range(len(Trips)):
        for j in range(len(Trips[i])):
            subTrip.append(p_data[Trips[i][j]])
            pass
        mTrip.append(subTrip)
        subTrip = []
        pass
    return mTrip
    pass

def calculateDistanceAcc(GPS1,GPS2):
    '''
        根据两个GPS点，计算当前速度和方向
        :param GPS1:
        :param GPS2:
        :return: 距离，加速度
        '''
    deltaTime = (GPS2[5] - GPS1[5]) * 24. * 3600
    if deltaTime == 0:
        deltaTime = 0.1
        print("deltaTime=0")
        pass
    A = (GPS1[0], GPS1[1])
    B = (GPS2[0], GPS2[1])
    # distance = vincenty(A, B).meters
    distance=GPS1[2]*deltaTime
    acc=(GPS2[2]-GPS1[2])/deltaTime

    return distance, acc
    pass

def calculateFeatures(p_data):
    for i in range(len(p_data)):
        for j in range(len(p_data[i])-1):
            GPS1=p_data[i][j]
            GPS2=p_data[i][j+1]
            distance,acc=calculateDistanceAcc(GPS1,GPS2)
            p_data[i][j].insert(7,distance)
            p_data[i][j].insert(8,acc)
            pass
        p_data[i][-1].insert(7, distance)
        p_data[i][-1].insert(8, acc)
        pass
    return p_data
    pass

def segmentTripByFeature(p_data,p_vthd,p_athd,p_dthd,p_tthd,p_N,p_scale):
    m_label=np.zeros((len(p_data)),dtype='int8')

    # 将所有可能的步行点都找出来
    for i in range(len(p_data)):
        if(p_data[i][2]<=p_vthd and abs(p_data[i][8])<=p_athd):
            m_label[i]=1
            pass
        pass

    m_Mthd=int(p_N*p_scale)

    # 根据前后关系，将部分点进行反转
    changeFlag=True
    while(changeFlag):
        changeFlag=False
        for i in range(len(p_data)):
            prePoint=max(0,i-p_N)
            postPoint=min(len(p_data)-1,i+p_N)
            walkRate=sum(m_label[prePoint:postPoint])/(postPoint-prePoint)
            if(m_label[i]==0 and walkRate>p_scale):
                m_label[i]=1
                changeFlag=True
                pass
            elif(m_label[i]==1 and walkRate<1-p_scale):
                m_label[i]=0
                changeFlag=True
                pass
            pass
        pass

    if(len(p_data)<2*p_N):
        return []

    # 可以寻找正或反变化
    func=0
    initial=0
    CTP=[0]
    for i in range(p_N,len(p_data)-p_N,1):
        prePoint = max(0, i - p_N)
        postPoint = min(len(p_data) - 1, i + p_N)
        preRate = sum(m_label[prePoint:i]) / (i - prePoint)
        postRate=sum(m_label[i:postPoint])/(postPoint-i)
        # 非步行-》步行
        if((func==0 or func==2) and preRate<1-p_scale and postRate>p_scale):
            CTP.append(i)
            func=1
            if(initial==0):
                # 首段非步行
                initial=1
            continue
            # 步行-》非步行
        if((func==0 or func==1 ) and preRate>p_scale and postRate<1-p_scale):
            CTP.append(i)
            func=2
            if(initial==0):
                # 首段步行
                initial=2
            pass
        pass
    CTP.append(len(p_data)-1)
    if(func==0):
        ratio= sum(m_label) / len(m_label)
        if(ratio>0.5):
            # 步行
            func=2
            initial=2
        else:
            # 非步行
            func=1
            initial=1


    trip={"label":[],"data":[]}
    trueInitial=2

    CTPS=[0]
    # 首段非步行
    if(initial==1):
        i=0
        first = True
        while(i<len(CTP)-1):
            start=CTP[i]
            end=CTP[i+1]
            deltaTime = (p_data[end][5] - p_data[start][5]) * 24. * 3600
            dist=0
            for j in range(start,end,1):
                dist=dist+p_data[j][7]
                pass
            if (dist/deltaTime < p_vthd+0.5):
                i = i + 2
                pass
            else:
                if(first):
                    CTPS.append(CTP[i + 1])
                    trueInitial = 1
                else:
                    CTPS.append(CTP[i])
                    CTPS.append(CTP[i + 1])
                i = i + 2
                pass
            first=False
            pass
        if(not CTPS[-1] == CTP[-1] ):
            CTPS.append(CTP[-1])
    # 首段步行
    else:
        i=1
        while (i < len(CTP) - 1):
            start = CTP[i]
            end = CTP[i + 1]
            deltaTime=(p_data[end][5]-p_data[start][5])* 24. * 3600
            dist = 0
            for j in range(start, end, 1):
                dist = dist + p_data[j][7]
                pass
            if (dist/deltaTime < p_vthd+0.5):
                i = i + 2
                pass
            else:
                CTPS.append(CTP[i])
                CTPS.append(CTP[i + 1])
                i = i + 2
                pass
            pass
        if (not CTPS[-1] == CTP[-1]):
            CTPS.append(CTP[-1])

    for i in range(len(CTPS)-1):
        if(len(trip['label'])==0 and trueInitial==1):
            trip["label"].append("non-walk")
            trip['data'].append(p_data[CTPS[i]:CTPS[i+1]+1])
            pass
        elif (len(trip['label'])==0 and trueInitial==2):
            trip["label"].append("walk")
            trip['data'].append(p_data[CTPS[i]:CTPS[i + 1]+1])
        elif(trip['label'][-1]=="non-walk"):
            trip['label'].append("walk")
            trip['data'].append(p_data[CTPS[i]:CTPS[i + 1]+1])
        elif(trip['label'][-1]=="walk"):
            trip['label'].append("non-walk")
            trip['data'].append(p_data[CTPS[i]:CTPS[i + 1]+1])
            pass
    return trip
    pass

def getFinalTag(p_data):
    if p_data==[]:
        return
    dataFeature=[]
    busStops=[(42.362050,-71.091445),(42.362670,-71.088181)]

    # 计算数据特征
    for i in range(len(p_data['label'])):
        max_speed=0
        min_speed=100
        max_acc=0
        min_acc=100
        dist=0
        deltaTime=0
        averageSpeed=0
        for j in range(len(p_data['data'][i])):
            currentItem=p_data['data'][i][j]
            if(currentItem[2]<min_speed):
                min_speed=currentItem[2]
                pass
            if(currentItem[2]>max_speed):
                max_speed=currentItem[2]
                pass
            if(abs(currentItem[8])>max_acc):
                max_acc=abs(currentItem[8])
                pass
            if(abs(currentItem[8]<min_acc)):
                min_acc=abs(currentItem[8])
            dist=dist+currentItem[7]
            pass
        deltaTime=(p_data['data'][i][-1][5]-p_data['data'][i][0][5])* 24. * 3600
        averageSpeed=dist/deltaTime
        dataFeature.append([min_speed,max_speed,min_acc,max_acc,dist,averageSpeed,deltaTime])
        pass

    # 判断骑车
    for i in range(len(p_data['label'])):
        if(p_data['label'][i]=="non-walk"):
            # 自行车
            if(dataFeature[i][1]<6 and dataFeature[i][5]<5):
                p_data['label'][i]='bike'
                pass
        pass

    # 判断公交站
    busCnt=np.zeros((len(busStops)),dtype='int8')
    for i in range(len(p_data['label'])):
        if(p_data['label'][i]=='walk'):
            for j in range(len(p_data['data'][i])):
                for k in range(len(busStops)):
                    di=vincenty((p_data['data'][i][j][0],p_data['data'][i][j][1]), busStops[k]).meters
                    #
                    if(di<10):
                        busCnt[k]+=1
                pass
            pass
        pass

    # 判断开车
    for i in range(len(p_data['label'])):
        if (p_data['label'][i] == "non-walk"):
            # 开车
            if (dataFeature[i][1] > 10 and dataFeature[i][5] > 4):
                p_data['label'][i] = 'car'
                pass
        pass

    # 合并非走路项
    changeFlag=True
    while(changeFlag):
        changeFlag=False
        for i in range(len(p_data['label'])-2):
            if(p_data['label'][i]==p_data['label'][i+2] and ( not p_data['label'][i]=='walk') and ( not p_data['label'][i]=='walk') and p_data['label'][i+1]=='walk'):
                p_data['label'][i+1]=p_data['label'][i]
                changeFlag=True
                pass
            pass
        pass
    return p_data
    pass

def dataDescribe(data):
    """
    统计预测后当天的各种出行方式距离
    """
    distance={"walk":0,"bike":0,"subway":0,"bus":0,"car":0,"non-walk":0}
    time={"walk":0,"bike":0,"subway":0,"bus":0,"car":0,"non-walk":0}
    for i in range(len(data)):
        if(data[i]==None):
            continue
        for j in range(len(data[i]['label'])):
            for k in range(len(data[i]['data'][j])):
                distance[data[i]['label'][j]]=distance[data[i]['label'][j]]+data[i]['data'][j][k][7]
                time[data[i]['label'][j]] = time[data[i]['label'][j]]+1*2
            pass
        pass
    print(distance)
    print(time)
    pass

def dataAccuracy(data):
    """
    统计预测的结果与真实标签的相似度
    """
    # 实际为走路，预测为走路、骑车、地铁、公交、汽车、其他
    confusionMatrix={'walk'  :{'walk':0,'bike':0,'subway':0,'bus':0,'car':0,'non-walk':0},
                     'bike'  :{'walk':0,'bike':0,'subway':0,'bus':0,'car':0,'non-walk':0},
                     'subway':{'walk':0,'bike':0,'subway':0,'bus':0,'car':0,'non-walk':0},
                     'bus'   :{'walk':0,'bike':0,'subway':0,'bus':0,'car':0,'non-walk':0},
                     'car'   :{'walk':0,'bike':0,'subway':0,'bus':0,'car':0,'non-walk':0}}

    for i in range(len(data)):
        if(data[i]==None):
            continue
        for j in range(len(data[i]['label'])):
            for k in range(len(data[i]['data'][j])):
                currentItem=data[i]['data'][j][k]
                confusionMatrix[currentItem[9]][data[i]['label'][j]]+=1
                pass
            pass
        pass
    tag=['walk','bike','subway','bus','car','non-walk']
    num=0
    for i in confusionMatrix:
        divide=confusionMatrix[i][tag[0]]+confusionMatrix[i][tag[1]]+confusionMatrix[i][tag[2]]+confusionMatrix[i][tag[3]]+confusionMatrix[i][tag[4]]+confusionMatrix[i][tag[5]]
        if divide==0:
            acc=0
        else:
            acc=confusionMatrix[i][i]/divide
        print("{0} {1}, Accuracy: {2}".format(tag[num], confusionMatrix[i], acc))
        num+=1
    pass

if __name__ =='__main__':
    fileName="Database/User017/User017.txt"

    mData=readData(fileName)

    speed=50.0
    star=5
    mData_Filtered=filterData(mData, speed,star)

    interval=120
    data_segment_time=segmentTripByTime(mData_Filtered,interval)

    data_segment_feature=calculateFeatures(data_segment_time)

    vthd=2.0
    athd=0.6
    dthd=50
    tthd=20
    N=10
    scale=0.7
    data_subsegs_processed=[]
    for i in range(len(data_segment_feature)):
        data_subsegs=segmentTripByFeature(data_segment_feature[i],1.8,0.6,50,20,10,0.7)
        data_subsegs_processed.append(getFinalTag(data_subsegs))
        pass

    dataDescribe(data_subsegs_processed)
    dataAccuracy(data_subsegs_processed)