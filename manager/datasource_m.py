# -*- coding: utf-8 -*-
from base import datasource_b
import json
from common.utils import defaultencode
from common.base import get_module_object
import sys
reload(sys)
sys.setdefaultencoding('utf8')
_modules_split = 'datasource'

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
            old = datasource_b.get_data_by_name(data['name'],'',other)
            if old:
                if old['status'] == 1:
                    return {'status':0,'msg':u'相同名称的数据源已存在，请更换个其他名称'}
            data['user'] = 0
            data['status'] = 1
            try:
                if 'id' in data and data['id']:
                    result = datasource_b.update(data)
                else:
                    result = datasource_b.save(data)
                return {'status':1,'msg':u'保存成功','data':result}
            except Exception, e:
                return {'status':0,'msg':u'保存失败，请先检查是否名称重复，如不重复联系管理员'}
    return {'status':0,'msg':u'类型错误,未定义'}


#获取数据源信息
def get_datasource(sid,customs=""):
    data = datasource_b.get_data_by_id(sid)
    if len(data):
        objects = get_module_object(_modules_split)
        for item in objects:
            if objects[item].types == data['types']:
                return objects[item].get_datasource(data)
    return False

def get_datasource_other(data,types):
    objects = get_module_object(_modules_split)
    for item in objects:
        if objects[item].types == types:
            return objects[item].get_datasource_other(data)
    return data

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

#获取数据源列表
def get_list(sid="",name="",current=1,rowCount=20):
    data = datasource_b.get_datasource_list(sid,name,current=current,rowCount=rowCount)
    result = {}
    result['current'] = current
    result['rowCount'] = rowCount
    result['rows'] = []
    result['total'] = 0
    if data:
        for item in data:
            result['rows'].append(item)
        result['total'] = datasource_b.get_datasource_list(sid,name,iscount=True,current=current,rowCount=rowCount)
        return result
    return result
