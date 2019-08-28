import datetime
import xlrd
import re
from functools import reduce

# 清洗航班excel的数据
COL_DATE=0;
COL_TIME=6;
COL_TRAVELLER=13;



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
    return time,dic_traveller


def read_excel(path,row):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_name('sheet1')
    time,dic_traveller = read_excel_row(sheet,row)
    return time,dic_traveller


def get_data_on_date(path,date):
  
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_name('sheet1') 
    rows = sheet.nrows  #sheet页里面的行数
    key = date;

    dict_data = {}

    for row in range(1,rows):
        value = {}
        r_date = xlrd.xldate.xldate_as_datetime(sheet.cell(row,COL_DATE).value,0)
        r_date = str(r_date.year)+"-"+str(r_date.month)+"-"+str(r_date.day)
        # if(date == )
        if r_date == date:
            time,dic_traveller = read_excel_row (sheet,row)

            dict_data[time] = dic_traveller
        else:
            # 有风险，excel真的是按日期顺序排列下来的？
            break;
    print(dict_data)
    return;


get_data_on_date("airline.xls","2019-1-14")
# time,dic_traveller = read_excel("airline.xls",1)
# print(time)
# print(dic_traveller)