# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db
import os
from crontab import CronTab
from common.utils import dbFormatToDict
from common import cron_base
import time

_home_path = "/home/jianczhang/project/charts/"
_log_path = "./"
_autotype = 1
_handletype = 2
_command = "source ~/.bash_profile && cd "+_home_path+" && python run_task_single.py -i={} -d=$(date +\%s) -t=1 >/dev/null 2>&1"
_handle_command = "source ~/.bash_profile && cd "+_home_path+" && python run_task_single.py -i={} -d={} -t=2 -c=1 > /dev/null 2>&1;"
_error_msg = []
_cron  = CronTab(user=True)
#获取所有数据
def get_task():
    sql = "select * from t_chart_task where status in (1,2);"
    result = _metric_meta_db.query(sql)
    return result
#获取所有任务
def get_cron():
    cmd = "python task_to_cron.py"
    return _cron.find_command(cmd)

#检查是否超过时间
def is_between_range(data,cur):
    st = time.mktime(time.strptime(data['st'].isoformat(),'%Y-%m-%dT%X'))
    et = time.mktime(time.strptime(data['et'].isoformat(),'%Y-%m-%dT%X'))
    if st <= cur and et >= cur:
        return True
    return False

def is_timeout(data,cur):
    et = time.mktime(time.strptime(data['et'].isoformat(),'%Y-%m-%dT%X'))
    if ( cur - et )/86400 > 30:
        return True
    return False

def handle():
    now = time.time()
    tasks = get_task()
    crons = get_cron()
    tasks_dict = dbFormatToDict(tasks,'id')
    #删除已失效但未删除的任务
    for cron in crons:
        comment = cron.comment
        ids = comment.split("_")
        if len(ids) == 2 and int(ids[1]) == _autotype:
            tmp_id = ids[0]
            if tmp_id in tasks_dict:
                pass
            else:
                cron_base._del_job(comment)
    #生成新任务并删除失效任务
    for key in tasks_dict:
        item = tasks_dict[key]
        is_should_run = is_between_range(item,now)
        command = _command.format(item['id'],item['id'])
        comment = "{}_{}".format(item['id'],_autotype)
        if is_should_run:
            #新增任务
            if item['status'] == 1 and item['task_status'] in [0,2]:
                is_ok = True
                status = item['task_status']
                form = {}
                form['id'] = item['id']
                form['task_status'] = _autotype
                try:
                    _metric_meta_db.update('t_chart_task',where="id={}".format(form['id']),**form)
                except Exception, e:
                    is_ok = False
                if is_ok:
                    try:
                        cron_base._modify_job(comment,command,item['cron'])
                    except Exception, e:
                        is_ok = False
                    if is_ok:
                        pass
                    else:
                        _error_msg.append(u"{}设置crontab失败".format(item['id']))
                        form['task_status'] = status
                        _metric_meta_db.update('t_chart_task',where="id={}".format(form['id']),**form)
                else:
                    _error_msg.append(u"{}写入数据库失败".format(item['id']))
            #删除任务
            elif item['status'] == 2 and item['task_status'] in [0,1] :
                cron_base._del_job(comment)
        else:
            cron_base._del_job(comment)
        if is_timeout(item,now):
            form = {}
            form['id'] = item['id']
            form['status'] = 2
            form['task_status'] = 2
            form['user'] = -100
            _metric_meta_db.update('t_chart_task',where="id={}".format(form['id']),**form)
    return _error_msg

def run_single(tid,times):
    result = {'status':0,"msg":u"缺少必要参数"}
    if tid and times:
        command = _handle_command.format(tid,times,times,tid)
        comment = "{}_{}".format(tid,_handletype)
        cron_times = time.strftime("%M %H %d %m %w",time.localtime(time.time()+60))
        try:
            cron_base._modify_job(comment,command,cron_times)
            return {'status':1,"msg":u"设置成功"}
        except Exception, e:
            result =  {'status':0,"msg":u"手动设置{}的crontab失败".format(item['id'])}
    return result

def kill_task(tid,times,types):
    result = {'status':0,"msg":u"缺少必要参数"}
    if tid and times and types:
        command = r""" ps ux|grep "python run_task_single.py -i={} -d={} -t={}"|awk '{{print $2}}'|xargs kill -9 """.format(tid,times,types)
        p = os.system(command)
        if p:
            result = {'status':1,"msg":u"取消成功"}
        else:
            result = {'status':0,"msg":u"取消失败"}
    return result
