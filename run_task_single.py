# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db
import json
from base import task_b
from common import cron_base
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import argparse
from common.base import get_module_object
_modules_split="task"
_handletype = 2

#检查是否超过时间
def is_between_range(data,cur):
    st = time.mktime(time.strptime(data['st'].isoformat(),'%Y-%m-%dT%X'))
    et = time.mktime(time.strptime(data['et'].isoformat(),'%Y-%m-%dT%X'))
    if st <= cur and et >= cur:
        return True
    return False

def warning(ids,timestramp,types,msg):
    print u"params： -i='{}' -d={} -t={} ，msg：{}".format(ids,timestramp,types,msg)


#处理数据
def handle(ids,timestramp,types,clear):
    now = time.time()
    try:
        task = task_b.get_task(ids)
    except Exception, e:
        warning(ids,timestramp,types,u"获取此id数据失败，请查看id是否正确或数据库有无异常")
        return
    if task:
        if types == 2 or is_between_range(task,now):
            form = {}
            form['tid'] = ids
            form['types'] = types
            form['run_time'] = time.strftime("%Y-%m-%d %X",time.localtime(timestramp))
            form['st'] = time.strftime("%Y-%m-%d %X",time.localtime(now))
            log_id = task_b.init_task_log(form)
            objects = get_module_object(_modules_split)
            ishandle = False
            for item in objects:
                if objects[item].types == task['types']:
                    try:
                        run_result = objects[item].run_task(task,timestramp)
                        if type(run_result['status']) != int:
                            raise Warning
                    except Exception, e:
                        warning(ids,timestramp,types,u"此id对应的任务对应的处理代码错误，未正确返回结果")
                        return
                    form = {}
                    form['id'] = log_id
                    form['et'] = time.strftime("%Y-%m-%d %X",time.localtime())
                    form['status'] = int(run_result['status'])+1
                    form['msg'] = run_result.get("msg","")
                    try:
                        ishandle = task_b.update_task_log(form)
                    except Exception, e:
                        warning(ids,timestramp,types,u"此id对应的任务运行结束后，更新失败")
                        return
                    comment = "{}_{}".format(ids,types)
                    if clear:
                        try:
                            cron_base._del_job(comment)
                        except Exception, e:
                            warning(ids,timestramp,types,u"删除{}任务失败".format(comment))
                            return
            if not ishandle:
                warning(ids,timestramp,types,u"此id对应的任务没有所对应的应用程序来处理")
                return
        else:
            warning(ids,timestramp,types,u"此id对应的任务不在规定的运行时间内")
            return
    else:
        warning(ids,timestramp,types,u"此id对应的任务不存在")
        return

if '__main__' == __name__:
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--id", 
            type=int, required=True,
            help="please input the task id.")
    parser.add_argument("-d", "--date", 
            type=int , required=True,help="please input the timestramp.")
    parser.add_argument("-t", "--type", 
            type=int , required=True,help="please input the type.the 1 is auto.the 2 is manual.the default is 1", default=1)
    parser.add_argument("-c", "--clear", 
            type=int,help="if once run ,please input it", default=0)
    args = parser.parse_args()
    handle(args.id,args.date,args.type,args.clear)
