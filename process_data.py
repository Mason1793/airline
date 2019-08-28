import datetime
import xlrd
import re
from functools import reduce
import time

# 清洗航班excel的数据
COL_DATE=0;
COL_TIME=6;
COL_TRAVELLER=13;
COL_PROPERTY=12; 

INTERNATIONAL = "国际"
DOMESTIC = "国内"
TIME_FLY = "time_fly"
PROPERTY = "property"
TRAVELLER="traveller"


def read_excel_row(sheet,row):
    dic_traveller = {}
    time = xlrd.xldate_as_tuple(sheet.cell(row,COL_TIME).value,0)
    traveller_str = sheet.cell(row,COL_TRAVELLER).value
    traveller_str = traveller_str.split('#')[1:]

    for line in traveller_str:
        pattern = r'(.*?)[[]'
        line_name = re.findall(re.compile(pattern),line)[0]

        count_arr = re.findall(re.compile(r'[[](.*?)[]]',re.S),line)
        count_arr_num = []
        count_info = {}
        for i in count_arr:
            key = line_name + "_" + i[0:1]
            value = i[2:]
            value = list(map(int,value.split(',')))
            value = reduce((lambda x,y:x+y),value)
            dic_traveller[key] = value
    return time,dic_traveller,


def read_excel(path,row):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_name('sheet1')
    time,dic_traveller = read_excel_row(sheet,row)
    return time,dic_traveller


def get_data_on_date(path,date):
  
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_name('一周历史航班数据') 
    rows = sheet.nrows  #sheet页里面的行数
    key = date;

    data_on_date = []

    for row in range(1,rows):
        value = {}
    
        r_date = xlrd.xldate.xldate_as_datetime(sheet.cell(row,COL_TIME).value,0)
        value[TIME_FLY] = str(r_date)
        r_date = str(r_date.year)+"-"+str(r_date.month)+"-"+str(r_date.day)

        prop=sheet.cell(row,COL_PROPERTY).value
        value[PROPERTY]=prop
        if r_date == date:
            time,traveller = read_excel_row (sheet,row)
            value[TRAVELLER]=traveller
            
            # dict_data[time] = dic_traveller
        else:
            # 有风险，excel真的是按日期顺序排列下来的？
            break
        data_on_date.append(value)
    
    data_on_date = sorted(data_on_date,key=lambda item: cmp(item),reverse=False)
    return data_on_date;

def cmp(item):
    t_time = item[TIME_FLY]
    t_time = datetime.datetime.strptime(t_time,'%Y-%m-%d %H:%M:%S')
    return t_time.hour,t_time.minute,t_time.second

# 某个时段的各种旅客的人数统计
def count_traveller(time_from,time_to,data):
    time_from=time.mktime(datetime.datetime.strptime(time_from,'%Y-%m-%d %H:%M:%S').timetuple())
    time_to=time.mktime(datetime.datetime.strptime(time_to,'%Y-%m-%d %H:%M:%S').timetuple())
    cnt_dometic_economy_class=0;
    cnt_dometic_business_class=0;
    cnt_internationl_economy_class=0;
    cnt_internationl_business_class=0;
    
    
    for d in data:
        tar_time=d[TIME_FLY];
        tar_time=time.mktime(datetime.datetime.strptime(tar_time,'%Y-%m-%d %H:%M:%S').timetuple())
       
        if tar_time-time_from>0 and time_to-tar_time>0:
            print(d)
            traveler=d[TRAVELLER].items()
            prop=d[PROPERTY]
            for item in traveler:
                cnt = item[1]
                t_type = item[0]
                if t_type[-1]=='Y' and prop==DOMESTIC:
                    cnt_dometic_economy_class+=cnt
                elif t_type[-1]=='Y' and prop==INTERNATIONAL:
                    cnt_internationl_economy_class+=cnt
                elif t_type[-1]!='Y' and prop==DOMESTIC:
                    cnt_dometic_business_class+=cnt
                else:
                    cnt_internationl_business_class+=cnt

            

    return cnt_dometic_economy_class,cnt_dometic_business_class,cnt_internationl_economy_class,cnt_internationl_business_class




# # d = {'lille':25,'wangyang':21,'liqun':32,'lidaming':19}

# # d = sorted(d.items(),key = lambda item:item[1],reverse=False);
# print(d)
if __name__ == '__main__':
    data = get_data_on_date("/Users/mason/Desktop/airline.xls","2019-1-14")

    x,y,z,s = count_traveller("2019-01-14 00:00:00","2019-01-14 00:30:00",data)
    print("国内经济,国内商务，国际经济，国际商务")
    print(x,",",y,",",z,",",s)
# time,dic_traveller = read_excel("airline.xls",1)
# print(time)
# print(dic_traveller)