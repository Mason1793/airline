# 时间表示法
# 1-23,周一的[23,24]这个时间段
# 排班表表示
# {
#   1:[(1-0,1-10),(2-3,2-11)]
#   2:[(2-3,2-10),(3-23,4-9)]
# }
#  第一个人值班，周一0点 - 周一10点，周二3点 - 周二11点


array_counter=[7,4,2,2,6,10,15,15,10,8,12,16,20,14,13,10,12,10,11,10,5,4,2,2]
dict_schedule_total={
    1:[("1_0","1_10"),("2_3","2_11")],
    2:[("2_3","2_10"),("3_23","4_9")]
}

for weekday in range(1,7):
    for time in  range(0,23):
        cnt_couter_need=array_counter[time]
        
        print()


# 统计排班表中某个时间段在工作的人数
def cnt_worker_on_time(weekday_from,weekday_to,time_from,time_to):
    cnt=0
    worker_no=1
    for peroson_schedule in dict_schedule_total.values():
        for v in peroson_schedule:
           weekday_start=float(v[0].split('_')[0])
           weekday_end=float(v[1].split('_')[0])
           time_start=float(v[0].split('_')[1])
           time_end=float(v[1].split('_')[1])
           if weekday_start<weekday_from and weekday_end>weekday_to:
               cnt+=1
               break
           elif weekday_start==weekday_from and weekday_end<weekday_to and time_start<=time_from:
               cnt+=1
               break
           elif weekday_start<weekday_from and weekday_end==weekday_to and time_end>=time_to:
               cnt+=1
               break
           elif weekday_start==weekday_from and weekday_end==weekday_to and time_start<=time_from and time_end>=time_to:
               cnt+=1
               break

        worker_no+=1
        
    return cnt

if __name__ == '__main__':
    print(cnt_worker_on_time(4,4,0,0))



