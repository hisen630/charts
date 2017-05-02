# -*- coding: utf-8 -*-

'''获取当前日期前后N天或N月的日期'''

import time
import calendar
import re
_custome_tag = {
    'S':1,
    'M':60,
    'H':3600,
    'd':86400,
    'w':604800,
    'm':-1,
    'Y':-1
}
_format = {
    'Y':"%Y",
    "m":"%m",
    "d":"%d",
    "H":"%H",
    "M":"%M",
    "S":"%S",
    "s":""
}
_parse_num = re.compile(r"(\d+)(\w)")
_now = time.time()
class TimeCac():
    '''
        timestramp format="YYYY-MM-DD HH:MM:SS"
    '''
    def __init__(self,timestramp=None):
        if not timestramp:
            timestramp = time.time()
        self.time = time.localtime(timestramp)
        self.year = time.strftime("%Y", self.time)
        self.mon = time.strftime("%m", self.time)
        self.day = time.strftime("%d", self.time)
        self.hour = time.strftime("%H", self.time)
        self.min = time.strftime("%M", self.time)
        self.sec = time.strftime("%S", self.time)
        self.suffix = " {}".format(time.strftime("%X", self.time))

    def timestramp(self):
        '''''
        get the timestramp
        '''''
        return time.mktime(self.time)

    def get_days_of_month(self,year, mon):
        '''''
        get days of month
        '''
        return calendar.monthrange(year, mon)[1]


    def get_firstday_of_month(self,year, mon):
        '''''
        get the first day of month
        '''
        days = "01"
        if (int(mon) < 10):
            mon = "0" + str(int(mon))
        arr = (year, mon, days)
        return time.mktime(time.strptime("-".join("%s" % i for i in arr)+self.suffix,"%Y-%m-%d %X"))


    def get_lastday_of_month(self,year, mon):
        '''''
        get the last day of month
        '''
        days = calendar.monthrange(year, mon)[1]
        mon = self.addzero(mon)
        arr = (year, mon, days)
        return time.mktime(time.strptime("-".join("%s" % i for i in arr)+self.suffix,"%Y-%m-%d %X"))


    def get_firstday_month(self,n=0):
        '''''
        get the first day of month from today
        n is how many months
        '''
        (y, m, d) = self.getyearandmonth(n)
        d = "01"
        arr = (y, m, d)
        return time.mktime(time.strptime("-".join("%s" % i for i in arr)+self.suffix,"%Y-%m-%d %X"))


    def get_lastday_month(self,n=0):
        '''''
        get the last day of month from today
        n is how many months
        '''
        return time.mktime(time.strptime("-".join("%s" % i for i in self.getyearandmonth(n))++self.suffix,"%Y-%m-%d %X"))


    def getyearandmonth(self,n=0):
        '''''
        get the year,month,days from today
        befor or after n months
        '''
        thisyear = int(self.year)
        thismon = int(self.mon)
        totalmon = thismon + n
        if (n >= 0):
            if (totalmon <= 12):
                days = str(self.get_days_of_month(thisyear, totalmon))
                totalmon = self.addzero(totalmon)
                return (self.year, totalmon, days)
            else:
                i = totalmon / 12
                j = totalmon % 12
                if (j == 0):
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self.get_days_of_month(thisyear, j))
                j = self.addzero(j)
                return (str(thisyear), str(j), days)
        else:
            if ((totalmon > 0) and (totalmon < 12)):
                days = str(self.get_days_of_month(thisyear, totalmon))
                totalmon = self.addzero(totalmon)
                return (self.year, totalmon, days)
            else:
                i = totalmon / 12
                j = totalmon % 12
                if (j == 0):
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self.get_days_of_month(thisyear, j))
                j = self.addzero(j)
                return (str(thisyear), str(j), days)


    def addzero(self,n):
        '''''
        add 0 before 0-9
        return 01-09
        '''
        nabs = abs(int(n))
        if (nabs < 10):
            return "0" + str(nabs)
        else:
            return nabs


    def get_today_month(self,n=0):
        '''''
        获取当前日期前后N月的日期
        if n>0, 获取当前日期前N月的日期
        if n<0, 获取当前日期后N月的日期
        date format = "YYYY-MM-DD"
        '''
        (y, m, d) = self.getyearandmonth(n)
        arr = [y, m, d]
        if (int(self.day) < int(d)):
            arr = [y, m, self.day]
        return time.mktime(time.strptime("-".join("%s" % i for i in arr)+self.suffix,"%Y-%m-%d %X"))

def get_time_range(mode,fromt,tot,timestramp=0):
    if timestramp:
        _now = int(timestramp)
    else:
        _now = time.time()
    result = ['','']
    result = get_time_by_tag(fromt,tot)
    if mode == 'absolute':
        result = get_time_by_absolute(result[0],result[1])
    return result
def get_time_by_tag(fromt,tot):
    result = ['','']
    if fromt and tot:
        # try:
            stime = str(round(float(parse_time(fromt))))
            etime = str(round(float(parse_time(tot))))
            result = [stime,etime]
        # except Exception, e:
        #     pass
    return result

def parse_time(data):
    if 'now' in data:
        now_time = int(_now)
        s_time = now_time
        if data == 'now':
            return now_time
        else:
            m = _parse_num.search(data)
            if m:
                num = int(m.group(1))
                tag = m.group(2)
                cacl = "-"
                if "+" in data:
                    cacl = "+"
                if num>0 and tag:
                    unit = _custome_tag[tag]
                    if unit>0:
                        if cacl == '-':
                            s_time = s_time - unit*num
                        else:
                            s_time = s_time + unit*num
                    else:
                        if tag == 'Y':
                            s_time = get_month(s_time,num*12,cacl)
                        elif tag == 'm':
                            s_time = get_month(s_time,num,cacl)
                    if '/' in data:
                        tmp = data.split("/")
                        if tmp[1]:
                            return get_near_time(s_time,tmp[1])
                    return s_time
    return int(_now)
    
def get_month(s_time,num,cacl):
    tm = TimeCac(s_time)
    if cacl == "-":
        num = num*-1
    return tm.get_today_month(num)

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

def get_near_time(s_time,tag):
    if tag:
        if tag == 'S':
            return s_time
        else:
            tmp_time = list(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(s_time)))
            if tag == 'M':
                tmp_time[17:19] = '00'
            elif tag == 'H':
                tmp_time[14:] = '00:00'
            elif tag == 'd':
                tmp_time[11:] = '00:00:00'
            elif tag == 'w':
                for i in range(0,7):
                    if time.localtime((s_time-i*3600)).tm_wday == 0:
                        tmp_time = list(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime((s_time-i*3600))))
                tmp_time[11:] = '00:00:00'
            elif tag == 'm':
                tmp_time[8:19] = '01 00:00:00'
            elif tag == 'Y':
                tmp_time[5:19] = '01-01 00:00:00'
            return int(time.mktime(time.strptime("".join(tmp_time),"%Y-%m-%d %H:%M:%S")))
    return st

def get_time(params,timestramp=0):
    param = params.split("/",2)
    param_len = len(param)
    if param_len > 1:
        end = ""
        if param_len == 3:
            [stime,etime] = get_time_range('quick',"/".join(param[0:2]),"now",timestramp=timestramp)
            end = param[2]
        elif param_len == 2:
            [stime,etime] = get_time_range('quick',"/".join(param[0:1]),"now",timestramp=timestramp)
            end = param[1]
        stime_sec = stime
        stime = time.localtime(stime_sec)
        if end in _format:
            if end == 's':
                return int(stime_sec)
            else:
                pos = _format_time.find(end,0)
                stime = time.strftime(_format_time[0:pos+1],stime)
        else:
            if r"%" in end:
                stime = time.strftime(end,stime)
        return stime
    else:
        return params