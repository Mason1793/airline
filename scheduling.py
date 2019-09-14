import numpy as np
# 时间表示法
# 1-23,周一的[23,24]这个时间段
# 排班表表示
# {
#   1:[(1-0,1-10),(2-3,2-11)]
#   2:[(2-3,2-10),(3-23,4-9)]
# }
#  第一个人值班，周一0点 - 周一10点，周二3点 - 周二11点


array_counter=[7,4,0,0,6,10,15,15,10,8,12,16,20,14,13,10,12,10,11,10,5,4,2,2]
dict_schedule_total=np.zeros(52,30)

dict_work_time_schedule={
    "a":["4:25","13:00"],
    "b":["5:00","16:00"],

    "c":["7:00","18:00"],
    "d":["8:00","19:00"],
    "e":["9:00","20:00"],
    "f":["10:00","20:00"],

    "g":["14:00","0:00"],
    "h":["16:00","3:00"]
}


for day in range(0,29):
    for class_work in dict_work_time_schedule.keys():
        if is_necessary_for_class_work_on_day(class_work,day):
            schedule_worker_in_time_bucket(day,class_work)
       


# 安排工作人员的排班
def schedule_worker_in_time_bucket(day,class_work):
    for worker_no in range(1,52):

        if day>1 and dict_schedule_total[worker_no][day-1]!=None and dict_schedule_total[worker_no][day-1]!="":
            if class_work=="a" or class_work=="b" or class_work=="c":
                dict_schedule_total[worker_no][day]=class_work
                break
            elif class_work=="d" and dict_schedule_total[worker_no][day-1]!="a":
                dict_schedule_total[worker_no][day]=class_work
                break
            elif (class_work=="e" or class_work=="f") and dict_schedule_total[worker_no][day-1]!="a" and dict_schedule_total[worker_no][day-1]!="b":
                dict_schedule_total[worker_no][day]=class_work
                break
            elif (class_work=="g" or class_work=="h") and (dict_schedule_total[worker_no][day-1]=="g" or dict_schedule_total[worker_no][day-1]=="h"):
                dict_schedule_total[worker_no][day]=class_work
                break
        elif day==1:
            dict_schedule_total[worker_no][day]=class_work
            break
        elif day>1 and dict_schedule_total[worker_no][day-1]==None or dict_schedule_total[worker_no][day-1]=="":
            dict_schedule_total[worker_no][day]=class_work
            break


# 判断在某一天，是否还需要安排某个班次
# 我也知道写的有点傻气，抽空再改吧=。=，完成任务要紧
def is_necessary_for_class_work_on_day(class_work,day):
    cnt_array=np.zeros(1,8)
    
    for i in range(0,51):
        v=dict_schedule_total[i][day]
        if v==None or v=="":
            continue
        else:
            index_for_v=v-'a'
            cnt_array[index_for_v]=cnt_array[index_for_v]+1

    index=class_work-'a'
    cnt_array[index]=cnt_array[index]+1

    if cnt_array[0]>array_counter[5]:
        return False
    if cnt_array[0]+cnt_array[1]>max(array_counter[6],[7]):
        return False
    if cnt_array[1]+cnt_array[2]>array_counter[8]:
        return False
    if cnt_array[0]+cnt_array[2]+cnt_array[3]>array_counter[9]:
        return False
    if cnt_array[0]+cnt_array[1]+cnt_array[2]+cnt_array[3]+cnt_array[4]>array_counter[10]:
        return False
    if cnt_array[0]+cnt_array[1]+cnt_array[3]+cnt_array[4]+cnt_array[5]>array_counter[11]:
        return False
    if cnt_array[1]+cnt_array[2]+cnt_array[4]+cnt_array[5]>array_counter[12]:
        return False
    if cnt_array[0]+cnt_array[2]+cnt_array[3]+cnt_array[5]>array_counter[13]:
        return False
    if cnt_array[0]+cnt_array[1]+cnt_array[2]+cnt_array[3]+cnt_array[4]>array_counter[14]:
        return False
    if cnt_array[0]+cnt_array[1]+cnt_array[3]+cnt_array[4]+cnt_array[5]+cnt_array[6]>array_counter[15]:
        return False
    if cnt_array[1]+cnt_array[2]+cnt_array[4]+cnt_array[5]+cnt_array[6]>array_counter[16]:
        return False
    if cnt_array[2]+cnt_array[3]+cnt_array[5]+cnt_array[7]>array_counter[17]:
        return False
    if cnt_array[2]+cnt_array[3]+cnt_array[4]+cnt_array[6]+cnt_array[7]>array_counter[18]:
        return False
    if cnt_array[3]+cnt_array[4]+cnt_array[5]+cnt_array[6]+cnt_array[7]>array_counter[19]:
        return False
    if cnt_array[4]+cnt_array[5]+cnt_array[6]>array_counter[20]:
        return False
    if cnt_array[7]>max(array_counter[21],max(array_counter[0],max(array_counter[1],max(array_counter[2],array_counter[3])))):
        return False
    if cnt_array[6]+cnt_array[7]>max(array_counter[22],array_counter[23]):
        return False


    return True

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



