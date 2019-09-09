#!/bin/env python3
#-*-coding:utf-8-*-
import requests
import datetime
import json
import pytz
from icalendar import Calendar, Event

# 在此处输入获取到的cookie
cookie = "JSESSIONID=XXXXX"

headers = {
"Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
"Connection": "keep-alive",
"Content-Length": "14",
"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
"Cookie": cookie,
"Host": "jxgl.sau.edu.cn",
"Origin": "https://jxgl.sau.edu.cn",
"Referer": "https://jxgl.sau.edu.cn/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default&su=183405010224",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"
}

url = "https://jxgl.sau.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"

# 根据课程的节数返回上课的时间
def GetCourseTime(time):
    course_time_dict = {
    '1-2': [[8, 20, 0], [10, 0, 0]],
    '3-4': [[10, 20, 0], [12, 0, 0]],
    '5-6': [[13, 30, 0], [15, 10, 0]],
    '7-8': [[15, 30, 0], [17, 0, 0]],
    '9-10': [[18, 10, 0], [19, 50, 0]],
    '7-10': [[15, 30, 0], [19, 50, 0]]
    }
    return course_time_dict[time][0], course_time_dict[time][1]

# 抓取课表信息并转换为字典
def GetCourseInfo_dict(data):
    request = requests.post(url, headers=headers, data=data)
    if request.status_code != 200:
        print("RESPONSE", request.status_code)
        print("ERROR! Check the cookie you input")
        exit(0)
    a = request.text
    b = json.loads(a)
    return b

# 返回上课的周的区间
def GetCourseTakeWeeks(week_num):
    if '-' in week_num: # A-B周区间内上课
        weekstart = int(week_num[0:week_num.find('-')])
        weekend = int(week_num[week_num.find('-')+1:week_num.find('周')])
    else: # 仅A周上课
        weekstart = weekend = int(week_num[0:week_num.find('周')])
    return weekstart, weekend

# 根据学期和周数返回这节课所在的天数
def GetCourseDate(year, semester, week, course_in_day_of_week):
    if semester == 1:
        start = datetime.datetime(year, 8, 31, 0) #2019.9.1.00
    else:
        start = datetime.datetime(year, 3, 1, 0) #2019.3.1.00
    for i in range(7):
        if start.weekday() == 0: # if the start day is monday
            break
        else:
            start = start + datetime.timedelta(days=1)
    time = start + datetime.timedelta(days=(week-1) * 7 + (course_in_day_of_week-1))
    print("{}.{}.{}".format(time.year, time.month, time.day), "星期", time.weekday()+1)
    return time

# 创建事件
def CreateEvent(calendar, course_weeks_start, course_weeks_end, year, semester, a):
    time_zone = pytz.timezone('Asia/Shanghai')
    course_in_day_of_week = int(a['xqj']) # 星期几
    course_begin_time, course_end_time = GetCourseTime(a['jcor'])   # 根据课程的节数返回上课的时间
    print("\n课程名称: ", a['kcmc'], "星期:", a['xqj'])
    print("该课程由第{}周上到第{}周".format(course_weeks_start, course_weeks_end))
    for week in range(course_weeks_start, course_weeks_end+1):
        print("第{}周:".format(week))
        course_date = GetCourseDate(year, semester, week, course_in_day_of_week)
        event = Event()
        event.add('summary', a['kcmc'])
        event.add('dtstart',datetime.datetime(course_date.year,
            course_date.month, course_date.day, course_begin_time[0], course_begin_time[1], course_begin_time[2], tzinfo=time_zone))
        event.add('dtend', datetime.datetime(course_date.year,
            course_date.month, course_date.day, course_end_time[0],course_end_time[1], course_end_time[2], tzinfo=time_zone))
        event.add('dtstamp', datetime.datetime(course_date.year,
            course_date.month, course_date.day, course_begin_time[0], course_begin_time[1], course_begin_time[2], tzinfo=time_zone))
        event.add('description', "周数:{},教师:{}".format(a['zcd'], a['xm']))
        event.add('location', a['cdmc'])
        calendar.add_component(event)
    return calendar

def ConvertCalendar(course_dict):
    calendar = Calendar()
    calendar.add('prodid', '-//My calendar product//mxm.dk//')
    calendar.add('version', '2.0')
    semester = int(course_dict['xsxx']['XQMMC'])
    year = int(course_dict['xsxx']['XNM'])
    for num in course_dict['kbList']:
        a = num
        week_string_list = a['zcd'].split(',')
        for week_string in week_string_list:
            course_weeks_start, course_weeks_end = GetCourseTakeWeeks(week_string)
            calendar = CreateEvent(calendar, course_weeks_start, course_weeks_end,  year, semester, a)

    output_file_name = '{}:{}-{}.ics'.format(course_dict['xsxx']['XH'], course_dict['xsxx']['XNMC'], course_dict['xsxx']['XQMMC'])
    output_file = open(output_file_name, 'wb')
    output_file.write(calendar.to_ical())
    output_file.close()
    print('Success write your calendar to', output_file_name)

def main():
    now = datetime.datetime.now()
    if now.month <= 1 or now.month >= 9:
        semester = "3"
    else:
        semester = "12"
    data = {"xnm": "{}".format(now.year), "xqm": semester}
    course_dict = GetCourseInfo_dict(data)
    ConvertCalendar(course_dict)

if __name__ == '__main__':
    main()
