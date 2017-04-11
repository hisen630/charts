# -*- coding: utf-8 -*-
import json
import time
import re
_custome_tag = {
    's':1,
    'M':60,
    'h':3600,
    'd':86400,
    'w':604800,
    'm':-1,
    'y':-1
}
_parse_num = re.compile(r"(\d+)(\w)")
_now = time.time()
def get_time_range(mode,fromt,tot,timestramp=0):
    if timestramp:
        _now = int(timestramp)
    else:
        _now = time.time()
    result = ['','']
    if mode == 'quick':
        result = get_time_by_tag(fromt,tot)
    elif mode == 'relative':
        result = get_time_by_tag(fromt,tot)
    elif mode == 'absolute':
        result = get_time_by_absolute(fromt,tot)
    return result
def get_time_by_tag(fromt,tot):
    result = ['','']
    if fromt and tot:
        # try:
            stime = str(parse_time(fromt))
            etime = str(parse_time(tot))
            result = [stime,etime]
        # except Exception, e:
        #     pass
    return result
    
def get_time_by_absolute(fromt,tot):
    result = ['','']
    if fromt and tot:
        try:
            stime = str(int(time.mktime(time.strptime(fromt,"%Y-%m-%d %H:%M:%S"))*1000))
            if tot == 'now':
                etime = str(int(_now*1000))
            else:
                etime = str(int(time.mktime(time.strptime(tot,"%Y-%m-%d %H:%M:%S"))*1000))
            result = [stime,etime]
        except Exception, e:
            pass
    return result


def parse_time(data):
    if 'now' in data:
        now_time = int(_now*1000)
        s_time = now_time
        if data == 'now':
            return now_time
        else:
            m = _parse_num.search(data)
            if m:
                num = int(m.group(1))
                tag = m.group(2)
                if num>0 and tag:
                    unit = _custome_tag[tag]
                    if unit>0:
                        s_time = s_time - unit*1000*num
                    else:
                        if tag == 'y':
                            s_time = get_year(s_time,num)
                        elif tag == 'm':
                            s_time = get_month(s_time,num)
                    if '/' in data:
                        tmp = data.split("/")
                        if tmp[1]:
                            return get_near_time(s_time,tmp[1])
                    return s_time
    return int(_now*1000)

def get_year(s_time,num):
    tmp_time = list(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(s_time/1000)))
    tmp_year = int("".join(tmp_time[0:4]))
    if tmp_year>1970:
        tmp_year = tmp_year - num
        tmp_time[0:4] = "%04d" % (tmp_year)
        try:
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
        except Exception, e:
            tmp_time[8:10] = "%02d" % (int("".join(tmp_time[8:10]))-1)
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
    return s_time

def get_month(s_time,num):
    year = num / 12
    if year:
        s_time = get_year(s_time,year)
    months = num % 12
    tmp_time = list(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(s_time/1000)))
    tmp_month = int("".join(tmp_time[5:7]))
    if months == 0:
        return s_time
    if tmp_month > months:
        tmp_month = tmp_month - months
        tmp_time[5:7] = "%02d" % tmp_month
        try:
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
        except Exception, e:
            tmp_time[8:10] = "%02d" % (int("".join(tmp_time[8:10]))-1)
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
    elif tmp_month == months:
        tmp_time[5:7] = "12"
        tmp_year[0:4] = "%02d" % (int("".join(tmp_time[0:4]))-1)
        if int(tmp_year[0:4])<=1970:
            return s_time
        try:
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
        except Exception, e:
            tmp_time[8:10] = "%02d" % (int("".join(tmp_time[8:10]))-1)
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
    else:
        months = months - tmp_month
        tmp_time[5:7] = "%02d" % (12-months)
        tmp_time[0:4] = "%02d" % (int("".join(tmp_time[0:4]))-1)
        if int("".join(tmp_time[0:4]))<=1970:
            return s_time
        try:
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
        except Exception, e:
            tmp_time[8:10] = "%02d" % (int("".join(tmp_time[8:10]))-1)
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
    return s_time


def get_near_time(s_time,tag):
    if tag:
        if tag == 's':
            return s_time
        else:
            tmp_time = list(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(s_time/1000)))
            if tag == 'M':
                tmp_time[17:19] = '00'
            elif tag == 'h':
                tmp_time[14:] = '00:00'
            elif tag == 'd':
                tmp_time[11:] = '00:00:00'
            elif tag == 'w':
                for i in range(0,7):
                    if time.localtime((s_time-i*3600000)/1000).tm_wday == 0:
                        tmp_time = list(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime((s_time-i*3600000)/1000)))
                tmp_time[11:] = '00:00:00'
            elif tag == 'm':
                tmp_time[8:19] = '01 00:00:00'
            elif tag == 'y':
                tmp_time[5:19] = '01-01 00:00:00'
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S"))*1000)
    return st