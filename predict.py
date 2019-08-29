import math
import datetime
import matplotlib.pyplot as plt
import numpy as np
import xlwt
from process_data import  get_data_on_date,count_traveller



denominator = 24*60*60



# 这里修改航班时间
def ratio_accumulate_traveller(take_off_time,interval_time) :
    t0=datetime.datetime.strptime(take_off_time,"%Y-%m-%d %H:%M:%S")

    t0_zero=t0-datetime.timedelta(hours=t0.hour,minutes=t0.minute,seconds=t0.second)
    print("t0相对于的0点时间",(t0-t0_zero).seconds)
    t0=(t0-t0_zero).seconds/denominator
    print("t0 转换到0-1空间:",t0)
    mu=43.68*math.pow(t0,4)-95.04*math.pow(t0,3)+71.64*math.pow(t0,2)-21.29*t0-0.7403
    sigma=2.44*math.pow(t0,3)-4.738*math.pow(t0,2)+3.179*t0-0.383
    sigma=abs(sigma)
    # print("mu:",mu)
    # print("sigma:",sigma)
    temp_x=(math.log(interval_time)-mu)/(sigma*pow(2,0.5))
    p=0.5 - 0.5*math.erf(temp_x)
    return p

if __name__ == '__main__':
    # print(ratio_accumulate_traveller("2019-1-14 08:00:00",0.56))
    
    X = np.linspace(0.00000001,0.2,100)
    Y=list(map(lambda x: ratio_accumulate_traveller("2019-1-14 03:20:00",x),X))
    plt.plot(X,Y)
    plt.show()  
    # data = get_data_on_date("/Users/mason/Desktop/airline.xls","2019-1-14")
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






