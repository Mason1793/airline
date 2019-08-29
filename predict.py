import math
import datetime
import matplotlib.pyplot as plt
import numpy as np
import xlwt
from process_data import  get_data_on_date,count_traveller



denominator = 24*60*60

##"00:00:00","00:30:00","01:00:00","01:30:00","02:00:00","02:30:00","03:00:00","03:30:00","04:00:00","04:30:00"
                

every_moment = ["05:00:00","05:30:00","06:00:00","06:30:00","07:00:00","07:30:00","08:00:00","08:30:00",
                "09:00:00","09:30:00","10:00:00","10:30:00","11:00:00","11:30:00","12:00:00","12:30:00","13:00:00",
                "13:30:00","14:00:00","14:30:00","15:00:00","15:30:00","16:00:00","16:30:00","17:00:00","17:30:00",
                "18:00:00","18:30:00","19:00:00","19:30:00","20:00:00","20:30:00","21:00:00","21:30:00","22:00:00",
                "22:30:00","23:00:00","23:30:00","00:00:00"]


# 这里修改航班时间
def ratio_accumulate_traveller(take_off_time,interval_time) :
    t0= take_off_time
    mu=43.68*math.pow(t0,4)-95.04*math.pow(t0,3)+71.64*math.pow(t0,2)-21.29*t0-0.7403
    sigma=2.44*math.pow(t0,3)-4.738*math.pow(t0,2)+3.179*t0-0.383
    # print("mu:",mu)
    # print("sigma:",sigma)
    temp_x=(math.log(interval_time + 0.00001)-mu)/(sigma*pow(2,0.5))
    p=0.5 - 0.5*math.erf(temp_x)
    return p

def count_interval_time(time_flys):
    moments_to_zero = []
    for moment in every_moment:                                                     ##算出没半个小时到0点的时间，并转换到0-1空间
        t = datetime.datetime.strptime(moment,"%H:%M:%S")
        t_zero = t - datetime.timedelta(hours=t.hour,minutes=t.minute,seconds=t.second)
        t = (t-t_zero).seconds/denominator
        moments_to_zero.append(t)
    moments_to_zero[-1] = 1                                                         ##24:00:00的比例为1
    
    time_flys_to_zero = []
    ##这里将每天航班的起飞时间映射到0-1空间
    for take_off_time in time_flys:
        t0=datetime.datetime.strptime(take_off_time,"%Y-%m-%d %H:%M:%S")
        t0_zero=t0-datetime.timedelta(hours=t0.hour,minutes=t0.minute,seconds=t0.second)
        t0=(t0-t0_zero).seconds/denominator
        time_flys_to_zero.append(t0)
    return moments_to_zero,time_flys_to_zero                        ##返回当天

##计算间隔人数
def count_interval_travellers(moments_to_zero,time_flys_to_zero,travellers_num):
    internal_people = {}                            ##用来存储每一时刻的人数
    internals = []                                  ##时刻间隔
    # print(time_flys_to_zero)
    # print(moments_to_zero)
    for i in range(len(every_moment)-1): 
        internal = every_moment[i] +' - ' + every_moment[i+1]
        internal_people[internal] = 0
        internals.append(internal)

    for i in range(len(time_flys_to_zero)):
        p = []
        take_off_time = time_flys_to_zero[i]
        for j in range(len(moments_to_zero)-1):                 ##遍历每一时刻
            moment = moments_to_zero[j]                              
            if take_off_time < moments_to_zero[1] and take_off_time >moments_to_zero[0]:            ##计算5:00-5:30这一段时间
                p1 = ratio_accumulate_traveller(take_off_time,0.0000001)            ##直接为0，不能计算对数
                p2 = ratio_accumulate_traveller(take_off_time,take_off_time - moments_to_zero[0])
                traveller_num = travellers_num[i] * (p1-p2)
                internal_people[internals[0]] =internal_people[internals[0]] + traveller_num
                break
            elif moment < take_off_time:
                # print(take_off_time-moment)
                p.append(ratio_accumulate_traveller(take_off_time,take_off_time - moment))              
        p.append(1)                         ##5:30-5:35
        if len(p) >=2:
            for i in range(len(p) -1):
                internal_people[internals[i]] = internal_people[internals[i]] + travellers_num[i] * (p[i+1] -p[i])      ##计算每个时间段人数

    print(internal_people)
    
    l=list(internal_people.values())

    # plt.bar(range(len(l)), l)
    print(len(every_moment))
    print(len(l))
    # every_moment=
    plt.plot(every_moment[1:],l)
    plt.show()
            


##计算实际旅客人数
def count_traveller_num(air_propertys,travellers):
    travellers_num = []
    for i in range(len(air_propertys)):
        num = sum(travellers[i].values())                   ##得到航班的买票数
        if air_propertys[i] == '国内':
            travellers_num.append(num * 0.95 * 0.91 * (0.26 + 0.74*0.25))           ##计算国内航班实际乘客数
        else:
            travellers_num.append(num * 0.95 * 0.55)
    return travellers_num

#计算一天每个时间点的人数
def count_model(data):
    time_flys = []
    air_propertys = []
    travellers = []
    for air_data in data:
        time_flys.append(air_data['time_fly'])
        air_propertys.append(air_data['property'])
        travellers.append(air_data['traveller'])
    # print("飞行时间：",time_flys)
    # print("飞机属性：",air_propertys)
    # print("旅客:",travellers)
    
    travellers_num = count_traveller_num(air_propertys,travellers)                      ##计算旅客实际乘机人数
    moments_to_zero,time_flys_to_zero = count_interval_time(time_flys)                  ##将时间转换为0-1空间上
    count_interval_travellers(moments_to_zero,time_flys_to_zero,travellers_num)         ##计算间隔人数

    
if __name__ == '__main__':
    data = get_data_on_date("/Users/mason/Desktop/补全航班数据.xls","2019-1-16")
    # print(data)
    count_model(data)
    # p = ratio_accumulate_traveller(0.24333,0.00001)
    # print(p)
    # print("时间格式YYYY-MM-DD hh-mm-ss,如2019-09-01 19:11:11")
    # print("输入起始时间：")
    # time_from=input()
    # print("输入结束时间：")
    # time_to=input()
    # x,y,z,s = count_traveller(time_from,time_to,data)
    # print("国内经济，国内商务，国际经济，国际商务")
    # print(x,",",y,",",z,",",s)
    # print("国内柜台，国际柜台")
    # m=(x+y)*(0.95*0.91)*(0.26+0.74*0.25)
    # n=(z+s)*(0.95*0.55)
    # print(m,n)



# X表示等待时间 ，等待时间为0无意义（ln0），需要设置一个极限值
# X=np.linspace(0.00000001,0.2,100)
# Y=list(map(lambda x: ratio_accumulate_traveller(x),X))
# plt.plot(X,Y)
# plt.show()


#2019-04-03 08:00:00






