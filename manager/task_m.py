# -*- coding: utf-8 -*-
from base import task_b
from common.base import get_module_object
import json
import time
from common.utils import defaultencode
from common import task_run_base
import sys
reload(sys)
sys.setdefaultencoding('utf8')
_modules_split = 'task'

#保存信息
def save(form):
    types = form.get("types",'')
    if types == '':
        return {'status':0,'msg':u'类型错误'}
    objects = get_module_object(_modules_split)
    for item in objects:
        if objects[item].types == int(types):
            data = objects[item].save_dict(form)
            if not data['status']:
                return data
            data = data['data']
            other = 0
            if 'id' in data and data['id']:
                other = data['id']
            old = task_b.get_data_by_name(data['name'],'',other)
            if old:
                if old['status'] == 1:
                    return {'status':0,'msg':u'相同名称的数据源已存在，请更换个其他名称'}
            data['user'] = 0
            data['status'] = 1
            data['task_status'] = 0
            try:
                if 'id' in data and data['id']:
                    result = task_b.update(data)
                else:
                    result = task_b.save(data)
                return {'status':1,'msg':u'保存成功','data':result}
            except Exception, e:
                return {'status':0,'msg':u'保存失败，请先检查是否名称重复，如不重复联系管理员'}
    return {'status':0,'msg':u'类型错误,未定义'}


#获取数据源信息
def get_datasource(sid,customs=""):
    data = task_b.get_data_by_id(sid)
    objects = get_module_object(_modules_split)
    for item in objects:
        if objects[item].types == data['types']:
            return objects[item].get_datasource(data)
    return False

#获取数据信息
def get_data(form,customs="",rows=0,istable=True):
    types = form.get("types",'')
    if types == '':
        return {'status':0,'msg':u'类型错误','data':[]}
    objects = get_module_object(_modules_split)
    for item in objects:
        if objects[item].types == int(types):
            return objects[item].get_data(form,customs,rows=rows,istable=istable)
    return False

#获取任务列表
def get_list(sid="",name="",current=1,rowCount=20):
    data = task_b.get_task_list(sid,name,current=current,rowCount=rowCount)
    result = {}
    result['current'] = current
    result['rowCount'] = rowCount
    result['rows'] = []
    result['total'] = 0
    if data:
        for item in data:
            result['rows'].append(item)
        result['total'] = task_b.get_task_list(sid,name,iscount=True,current=current,rowCount=rowCount)
        return result
    return result

#获取运行日志列表
def get_runlog_list(sid="",name="",current=1,rowCount=20):
    data = task_b.get_runlog_list(sid,name,current=current,rowCount=rowCount)
    result = {}
    result['current'] = current
    result['rowCount'] = rowCount
    result['rows'] = []
    result['total'] = 0
    if data:
        for item in data:
            result['rows'].append(item)
        result['total'] = task_b.get_runlog_list(sid,name,iscount=True,current=current,rowCount=rowCount)
        return result
    return result

def run_single(tid,lid,custom_time,opertype):
    result = {'status':0,"msg":u"缺少必要参数"}
    if opertype:
        if lid:
            loginfo = task_b.get_runlog_by_id(lid)
            tid = loginfo['tid']
            times = int(time.mktime(time.strptime("{}".format(loginfo['run_time']),"%Y-%m-%d %H:%M:%S")))
        else:
            if custom_time:
                times = int(time.mktime(time.strptime(custom_time,"%Y-%m-%d %H:%M:%S")))
            else:
                times = int(time.time())
        result = task_run_base.run_single(tid,times)
    return result

def run_cancel(lid):
    result = {'status':0,"msg":u"缺少必要参数"}
    if lid:
        loginfo = task_b.get_runlog_by_id(lid)
        loginfo['run_time'] = int(time.mktime(time.strptime("{}".format(loginfo['run_time']),"%Y-%m-%d %H:%M:%S")))
        result = task_run_base.kill_task(loginfo['tid'],loginfo['run_time'],loginfo['types'])
        if result['status'] == 1:
            form = {}
            form['id'] = lid
            form['status'] = 3
            try:
                task_b.update_task_log(form)
            except Exception, e:
                result = {'status':0,"msg":u"取消时，更新数据库失败"}
    return result
