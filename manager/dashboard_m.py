# -*- coding: utf-8 -*-
from base import chart_b,dashboard_b
from common import utils,mysql_base
import json
from common.utils import defaultencode,muti_data_trans
from gevent import monkey; monkey.patch_all()
from conf.default import _customs_name
import gevent
import chart_m
import cgi
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#获取列表，增加了整体json编码
def get_chart_list():
    charts = chart_b.get_chart_list(fields=['id','name'])
    result = []
    for item in charts:
        item['jsons'] = json.dumps(item,default=defaultencode)
        item['jsons'] = cgi.escape(item['jsons'],True)
        result.append(item)
    return result

def save(form):
    data = parse_params(form)
    if data['status'] == 0:
        return data
    else:
        data = data['data']
        other = 0
        if 'id' in data and data['id']:
            other = data['id']
        old = chart_b.get_data_by_name(data['name'],[1],other)
        if old:
            if old['status'] == 1:
                return {'status':0,'msg':u'相同名称的数据源已存在，请更换个其他名称'}
        data['user'] = 0
        data['status'] = 1
        if 'id' in data and data['id']:
            result = dashboard_b.update(data)
        else:
            result = dashboard_b.save(data)
        return {'status':1,'msg':u'保存成功','data':result}
#获取编辑页内容
def get_edit(sid):
    result = []
    if sid:
        data = dashboard_b.get_data_by_id(sid)
        if data:
            data['cids'] = json.loads(data['cids'])
            data['cinfo'] = []
            for item in data['cids']:
                cinfo = chart_b.get_data_by_id(item)
                data['cinfo'].append({"id":item,"name":cinfo['name']})
            result = data
    return result

#解析参数
def parse_params(form,check_conf=True):
    cid = form.get('id', '')
    name = form.get('name', '')
    ids = form.getlist("ids")
    data = {}
    msg = []
    if cid:
        data['id'] = cid
    if name.strip():
        data['name'] = name.strip()
    else:
        msg.append(u"未配置报表名")
    if ids:
        data['cids'] = json.dumps([int(item) for item in ids])
    else:
        msg.append(u"未选择报表")
    if msg:
        return {'status':0,'msg':";".join(msg)}
    else:
        return {'status':1,'data':data}

#根据提交内容获取数据
def get_data_by_form(form,istestcode=False):
    data = parse_params(form,False)
    if data['status'] == 0:
        return data
    keys = []
    data = data['data']
    for item in data['customs']:
        keys.extend(item.keys())
    if keys:
        source_data = datasource_b.get_data_by_ids(keys)
        result = get_data(data,source_data,istestcode)
    else:
        result = {'status':0,'msg':u'无数据源，请添加'}
    return result
#获取json的配置数据
def get_chart(did,customs=[],istable=False):
    if did:
        dinfo = dashboard_b.get_data_by_id(did)
        dinfo['cids'] = json.loads(dinfo['cids'])
        tmp_muti = {}
        global_customs = {}
        if u"0" in customs:
            global_customs = customs[u"0"]
        for item in dinfo['cids']:
            customs_split = {}
            if str(item) in customs:
                customs_split = customs[str(item)]
            istable = global_customs['istable'] if "istable" in global_customs else customs_split.get('istable',False) or istable
            offset = global_customs['offset'] if "offset" in global_customs else customs_split.get('offset',0)
            length = global_customs['length'] if "length" in global_customs else customs_split.get('length',0)
            customs_conbine = conbine_customs(customs_split.get('customs',[]),global_customs.get("customs",[]))
            tmp_muti[item] = gevent.spawn(chart_m.get_chart,str(item),customs_conbine,istable,offset=offset,length=length)
            
        gevent.joinall(tmp_muti.values())
        data = []
        msg = []
        for item in dinfo['cids']:
            if item in tmp_muti:
                p = tmp_muti[item].value
                if p:
                    data.append(p)
                else:
                    msg.append(u"报表id为\"{}\"的数据返回错误，程序运行中断".format(item))
        if msg:
            result = {'status':0,'msg':";".join(msg)}
        else:
            result = {"status":1,'msg':'','data':json.dumps(data,default=defaultencode)}
    else:
        result = {'status':0,'msg':u'dashboard id错误'}
    return result

def conbine_customs(old,new):
    if not old and not new:
        return []
    elif new and not old:
        return [{_customs_name:new}]
    elif old and not new:
        return old
    else:
        any_seq = -1
        for key,item in enumerate(old):
            for it in item:
                if it == _customs_name:
                    any_seq = key
        if any_seq>-1:
            old[any_seq][_customs_name] = mysql_base.combineCustom(old[any_seq][_customs_name],new)
            return old
        else:
            old.append({_customs_name:new})
            return old


#获取数据源列表
def get_list(sid="",name="",current=1,rowCount=20):
    data = dashboard_b.get_dashboard_list(sid,name,current=current,rowCount=rowCount)
    result = {}
    result['current'] = current
    result['rowCount'] = rowCount
    result['rows'] = []
    result['total'] = 0
    if data:
        for item in data:
            result['rows'].append(item)
        result['total'] = dashboard_b.get_dashboard_list(sid,name,iscount=True,current=current,rowCount=rowCount)
        return result
    return result
