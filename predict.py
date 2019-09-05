import math
import datetime
import matplotlib.pyplot as plt
import numpy as np
import xlwt
from process_data import  get_data_on_date,count_traveller



denominator = 24*60*60

##"00:00:00","00:30:00","01:00:00","01:30:00","02:00:00","02:30:00","03:00:00","03:30:00","04:00:00","04:30:00"
                

every_moment = ["00:00:00","00:30:00","01:00:00","01:30:00","02:00:00","02:30:00","03:00:00","03:30:00","04:00:00",
                "04:30:00","05:00:00","05:30:00","06:00:00","06:30:00","07:00:00","07:30:00","08:00:00","08:30:00",
                "09:00:00","09:30:00","10:00:00","10:30:00","11:00:00","11:30:00","12:00:00","12:30:00","13:00:00",
                "13:30:00","14:00:00","14:30:00","15:00:00","15:30:00","16:00:00","16:30:00","17:00:00","17:30:00",
                "18:00:00","18:30:00","19:00:00","19:30:00","20:00:00","20:30:00","21:00:00","21:30:00","22:00:00",
                "22:30:00","23:00:00","23:30:00","00:00:00"]


# 这里修改航班时间
def ratio_accumulate_traveller(take_off_time,interval_time) :
    t0= take_off_time
    mu=43.68*math.pow(t0,4)-95.04*math.pow(t0,3)+71.64*math.pow(t0,2)-21.29*t0-0.7403
    sigma=2.44*math.pow(t0,3)-4.738*math.pow(t0,2)+3.179*t0-0.383
    sigma = abs(sigma)
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
                # p1 = ratio_accumulate_traveller(take_off_time,0.0000001)            ##直接为0，不能计算对数
                # p2 = ratio_accumulate_traveller(take_off_time,take_off_time - moments_to_zero[0])
                # traveller_num = travellers_num[i] * (p1-p2)
                # internal_people[internals[0]] =internal_people[internals[0]] + traveller_num
                internal_people[internals[0]] = internal_people[internals[0]] + 0
                break
            elif moment < take_off_time:
                # print(take_off_time-moment)
                p.append(ratio_accumulate_traveller(take_off_time,take_off_time - moment))              
        p.append(1)                         ##5:30-5:35
        if len(p) >=2:
            for k in range(len(p) -1):
                internal_people[internals[k]] = internal_people[internals[k]] + travellers_num[i] * (p[k+1] -p[k])      ##计算每个时间段人数
                

    return internal_people
            


##计算实际旅客人数
def count_traveller_num(air_propertys,travellers):
    travellers_num = []
    for i in range(len(air_propertys)):
        num = sum(travellers[i].values())                   ##得到航班的买票数
        if air_propertys[i] == '国内':
            travellers_num.append(num * 0.95 * 0.91 * (0.26 + 0.74*0.25))           ##计算国内航班实际乘客数
            # print("国内:",num * 0.95 * 0.91 * (0.26 + 0.74*0.25))
        else:
            travellers_num.append(num * 0.95 * 0.55)
            # print("国际：",num * 0.95 * 0.55)
    return travellers_num


##分别计算国内国外四种类别的属性
def count_dome_inter_values(data):
    domestic_time_flys=[]                           ##国内航班起飞时间
    inter_time_flys = []                            ##国际航班起飞时间
    domestic_PFJC_travellers = []                   ##国内高端柜台人数
    domestic_GY_travellers =[]                      ##国内经济柜台人数
    inter_PFJC_travellers = []                      ##国际高端柜台人数
    inter_GF_travellers = []                        ##国内经济柜台人数

    for air_data in data:
        if air_data['property'] =='国内':
            domestic_GY_num = 0
            domestic_PFJC_num = 0
            domestic_time_flys.append(air_data['time_fly'])    
            for key in list(air_data['traveller'].keys()):        ##遍历所有键
                key = str(key)
                # print(keys[-1])
                if key[-1] =='G' or key[-1]=='Y':
                    
                    domestic_GY_num = domestic_GY_num + air_data['traveller'][key] 
                else:
                    domestic_PFJC_num = domestic_PFJC_num + air_data['traveller'][key] 
            domestic_GY_travellers.append(domestic_GY_num * 0.95 * 0.91 * (0.26 + 0.74*0.25))
            domestic_PFJC_travellers.append(domestic_PFJC_num * 0.95 * 0.91 * (0.26 + 0.74*0.25) + domestic_GY_num * 0.0525)          ##PFJC+金卡+白金卡
        else:
            inter_GY_num = 0
            inter_PFJC_num = 0
            inter_time_flys.append(air_data['time_fly'])
            for key in list(air_data['traveller'].keys()):
                key = str(key)
                if key[-1]=='G' or key[-1] =='Y':
                    # print(air_data['traveller'][key])
                    inter_GY_num = inter_GY_num + air_data['traveller'][key] 
                else:
                    inter_PFJC_num = inter_PFJC_num + air_data['traveller'][key]
            inter_GF_travellers.append(inter_GY_num * 0.95 * 0.55)
            inter_PFJC_travellers.append(inter_PFJC_num * 0.95 * 0.55 + inter_GY_num * 0.0525)   ##PFJC + 金卡 + 白金卡
    # print("国内高端柜台：",domestic_PFJC_travellers,"航班数：",len(domestic_PFJC_travellers))
    # print("国内经济柜台：",domestic_GY_travellers,"航班数：",len(domestic_GY_travellers))
    # print("国际高端柜台：",inter_PFJC_travellers,"航班数：",len(inter_PFJC_travellers))
    # print("国际经济柜台:",inter_GF_travellers,"航班数：",len(inter_GF_travellers))

    return domestic_time_flys,domestic_PFJC_travellers,domestic_GY_travellers,inter_time_flys,inter_PFJC_travellers,inter_GF_travellers



#计算一天每个时间点的人数
def count_model(data):
    domestic_time_flys,domestic_PFJC_travellers,domestic_GY_travellers,inter_time_flys,inter_PFJC_travellers,inter_GF_travellers = count_dome_inter_values(data)
   
    moments_to_zero,domestic_time_flys_to_zero = count_interval_time(domestic_time_flys)
    moments_to_zero,inter_time_flys_to_zero = count_interval_time(inter_time_flys)
    

    sum_domestic_PFJC_travellers = count_interval_travellers(moments_to_zero,domestic_time_flys_to_zero,domestic_PFJC_travellers)
    sum_domestic_GY_travellers = count_interval_travellers(moments_to_zero,domestic_time_flys_to_zero,domestic_GY_travellers)
    sum_inter_PFJC_travellers = count_interval_travellers(moments_to_zero,inter_time_flys_to_zero,inter_PFJC_travellers)
    sum_inter_GY_travellers = count_interval_travellers(moments_to_zero,inter_time_flys_to_zero,inter_GF_travellers)


    # print("国内高端柜台人数:",sum_domestic_PFJC_travellers,'\n')
    # print("国内经济柜台人数：",sum_domestic_GY_travellers,'\n')
    # print("国际高端柜台人数:",sum_inter_PFJC_travellers,'\n')
    # print("国际经济柜台人数：",sum_inter_GY_travellers,'\n')
    # moments_to_zero,time_flys_to_zero = count_interval_time(time_flys)                  ##将时间转换为0-1空间上
    # count_interval_travellers(moments_to_zero,time_flys_to_zero,travellers_num)         ##计算间隔人数
    


    time_flys = []
    air_propertys = []
    travellers = []
    for air_data in data:
        time_flys.append(air_data['time_fly'])
        air_propertys.append(air_data['property'])
        travellers.append(air_data['traveller'])
            
    travellers_num = count_traveller_num(air_propertys,travellers)                      ##计算旅客实际乘机人数
    moments_to_zero,time_flys_to_zero = count_interval_time(time_flys)                  ##将时间转换为0-1空间上
    sum_people = count_interval_travellers(moments_to_zero,time_flys_to_zero,travellers_num)         ##计算间隔人数
    print("总人数：",sum_people)

    l=list(sum_people.values())
    
    return sum_domestic_PFJC_travellers,sum_domestic_GY_travellers,sum_inter_PFJC_travellers,sum_inter_GY_travellers
    
    # plt.plot(every_moment[1:-1],l[:-1])
    # plt.title('2019-01-16')
    # plt.xticks(every_moment[1:-1],rotation=90)
   
    # plt.show()
    # print(time_flys)
    # print(inter_time_flys)
    # print(domestic_time_flys)

def plt_ratio(take_off_time):
    X=np.linspace(0.00000001,0.2,100)
    Y=list(map(lambda x: ratio_accumulate_traveller(take_off_time,x),X))
    plt.plot(X,Y)
    plt.show()
    return


# 绘制各个柜台的人数
def plt_CAPSS_tendency(sum_domestic_PFJC_travellers,sum_domestic_GY_travellers,sum_inter_PFJC_travellers,sum_inter_GY_travellers):
    X = np.arange(0,24,0.5)
    print(X)
    domestic_PFJC_Y = sum_domestic_PFJC_travellers.values()

    domestic_GY_Y = sum_domestic_GY_travellers.values()
    inter_PFJC_Y = sum_inter_PFJC_travellers.values()
    sum_inter_GY_travellers.values()
    # print(len(domestic_PFJC_Y))
   

    domestic_PFJC, = plt.plot(X,sum_domestic_PFJC_travellers.values(),c='red')
    domestic_GY, = plt.plot(X,sum_domestic_GY_travellers.values(),c='blue')
    inter_PFJC, = plt.plot(X,sum_inter_PFJC_travellers.values(),c='orange')
    inter_GY, = plt.plot(X, sum_inter_GY_travellers.values(),c='green')

    plt.xlabel("time")
    plt.ylabel("CAPSS")
    plt.legend(handles=[domestic_PFJC, domestic_GY,inter_PFJC,inter_GY], labels=['domestic_PFJC+vip', 'domestic_GY','inter_PFJC+vip','inter_GY'],loc='upper right')
    plt.show()
    return

def compute_Lq(S,rho_star,P0):
    Lq=(math.pow((S*rho_star),S)*(rho_star))/(math.factorial(S)*(1-rho_star)*(1-rho_star))
    Lq=Lq*P0;
    return Lq;

# 计算柜台数随着时间的安排变化
# cost_traveller 旅客等待的成本
# cost_counter 柜台的开放成本
# count_traveller 某类旅客的人数
# time_service 某台柜台的服务时间
# return c ,柜台数随时间的分布（30min）
# 算法描述：L(c)-L(c+1) <= cost_counter/cost_traveller <= L(c-1)-L(c)
# 排队论计算Lq
# 用不等式逼近c
# 详情请见说明文档（.md）
def compute_counter(cost_traveller,cost_counter,count_traveller,time_service):
    MAX_COUNT = 100
    threshold = cost_counter/cost_traveller
    _lambda = count_traveller*2 #人/小时
    mu = 1/time_service * 3600 #人/小时
    rho = _lambda/(mu) #服务强度，要小于1
    for c in range(2,MAX_COUNT,1):
        if(rho/c<1):
            part1=0
            for k in range(0,c-1):
                part1+=(1/math.factorial(k))*math.pow(rho,k)
            
            part2=(1/math.factorial(c))*(1/(1-rho/c))*(math.pow(rho,c))
            
            P0 = 1/(part1+part2);
            
            Lq=compute_Lq(c,rho/c,P0);
            Lq_before=compute_Lq(c-1,rho/(c-1),P0)
            Lq_after=compute_Lq(c+1,rho/(c+1),P0)

    
            if(Lq-Lq_after<=threshold and Lq_before-Lq>=threshold):
                return c;
    
    return 1; 

def statistics_counter(sum_domestic_PFJC_travellers,sum_domestic_GY_travellers,sum_inter_PFJC_travellers,sum_inter_GY_travellers):
    print("统计柜台数")
    demestic_counter={}
    international_counter={}
    high_end_counter={}

    cost_traveller=14.37
    cost_counter=15

    for key in sum_domestic_GY_travellers.keys():
        high_end_counter[key]=0+compute_counter(cost_traveller,cost_counter,sum_domestic_PFJC_travellers[key],120)
        high_end_counter[key]=high_end_counter[key]+compute_counter(cost_traveller,cost_counter,sum_inter_PFJC_travellers[key],120)
       
        demestic_counter[key]=0+compute_counter(cost_traveller,cost_counter,sum_domestic_GY_travellers[key],60)
        international_counter[key]=0+compute_counter(cost_traveller,cost_counter,sum_inter_GY_travellers[key],90)
    
    X = np.arange(0,24,0.5)
    l1,=plt.plot(X,high_end_counter.values(),c='red')
    l2,=plt.plot(X,demestic_counter.values(),c='blue')
    l3,=plt.plot(X,international_counter.values(),c='green')
    plt.xlabel("time")
    plt.ylabel("counter")

    plt.legend(handles=[l1,l2,l3], labels=['high-end', 'demestic','international'],loc='upper right')
    plt.show()
    return 

if __name__ == '__main__':
    data = get_data_on_date("补全航班数据.xls","2019-1-14")
    # plt_ratio(5/24)
    # count_dome_inter_values(data)
    sum_domestic_PFJC_travellers,sum_domestic_GY_travellers,sum_inter_PFJC_travellers,sum_inter_GY_travellers = count_model(data)
    
    statistics_counter(sum_domestic_PFJC_travellers,sum_domestic_GY_travellers,sum_inter_PFJC_travellers,sum_inter_GY_travellers)
    # val = list(sum_domestic_GY_travellers.values())
    # c = compute_counter(14.37,15,val[2],60)
    # print("机场人数：",val[2],"值机柜台数：",c)
    # 
    # count_model(data) 
    # plt_CAPSS_tendency(sum_domestic_PFJC_travellers,sum_domestic_GY_travellers,sum_inter_PFJC_travellers,sum_inter_GY_travellers)
    # count_model(data)
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



#2019-04-03 08:00:00






