import math
import datetime
import matplotlib.pyplot as plt
import numpy as np
import xlwt
import excel as xl



denominator = 24*60*60

def ratio_accumulate_traveller(interval_time):   
    temp_x=(math.log(interval_time)-mu)/(sigma*pow(2,0.5))
    p=0.5 - 0.5*math.erf(temp_x);
    return p




# 这里修改航班时间
t0=datetime.datetime.strptime("2019-04-03 21:20:00","%Y-%m-%d %H:%M:%S")

t0_zero=t0-datetime.timedelta(hours=t0.hour,minutes=t0.minute,seconds=t0.second)
print("t0相对于的0点时间",(t0-t0_zero).seconds)
t0=(t0-t0_zero).seconds/denominator
print("t0 转换到0-1空间:",t0);
mu=43.68*math.pow(t0,4)-95.04*math.pow(t0,3)+71.64*math.pow(t0,2)-21.29*t0-0.7403
sigma=2.44*math.pow(t0,3)-4.738*math.pow(t0,2)+3.179*t0-0.383
print("mu:",mu)
print("sigma:",sigma)

# X表示等待时间 ，等待时间为0无意义（ln0），需要设置一个极限值
X=np.linspace(0.00000001,0.2,100)
Y=list(map(lambda x: ratio_accumulate_traveller(x),X))
plt.plot(X,Y)
plt.show()


#2019-04-03 08:00:00






