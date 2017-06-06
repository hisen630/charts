# -*- coding: utf-8 -*-
from base import chart_b,dashboard_b,datasource_b
from common import utils,mysql_base
import json
from common.utils import defaultencode,muti_data_trans,dbFormatToDict
from gevent import monkey; monkey.patch_all()
from conf.default import _customs_name
import gevent
import chart_m
import cgi
import sys
import md5
reload(sys)
sys.setdefaultencoding('utf8')

#获取列表，增加了整体json编码
def get_chart_list():
    charts = chart_b.get_chart_list(fields=['id','name','customs'],rowCount=0)
    result = []
    dids_relation = {}
    dids = []
    for item in charts:
        customs = json.loads(item['customs'])
        dids_relation[item['id']] = []
        for it in customs:
            for i in it:
                dids_relation[item['id']].append(i)
                dids.append(i)
        result.append(item)
    datasource = datasource_b.get_datasource_list(dids,rowCount=0)
    datasource = dbFormatToDict(datasource,"id")
    for item in result:
        customs = {}
        if item['id'] in dids_relation:
            for it in dids_relation[item['id']]:
                it = int(it)
                if it in datasource and datasource[it]['conf']:
                    conf = json.loads(datasource[it]['conf'])
                    tmp = parse_customs(conf.get("customs",""))
                    customs = dict(customs,**tmp)
        tmp = item
        tmp['customs'] = customs
        item['conf'] = json.dumps(tmp)
    return result

def parse_customs(customs):
    result = {}
    if customs:
        tmp = customs.strip().split(";")
        for item in tmp:
            t = item.strip().split(":")
            if t[0].strip():
                result[t[0].strip()] = True
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
            if data['globals'].strip():
                data['globals'] = json.loads(data['globals'])
            else:
                data['globals'] = []
            tmp_list = []
            for item in data['globals']:
                t = json.loads(item)
                tmp=dict(t)
                tmp['globals'] = item
                tmp_list.append(tmp)
            data['globals'] = tmp_list
            data['cinfo'] = []
            for item in data['cids']:
                try:
                    item = int(item)
                    cinfo = chart_b.get_data_by_id(item)
                    data['cinfo'].append({"id":item,"name":cinfo['name'],"value":item})
                except Exception, e:
                    item = item.strip()
                    if ":" in item:
                        [name,iframe] = item.split(":",1)
                        m1 = md5.new()   
                        m1.update(name)
                        iframe = iframe.replace("\"","&quot;")
                        data['cinfo'].append({"id":m1.hexdigest(),"name":name,"value":name+":"+iframe})
            result = data
    return result

#解析参数
def parse_params(form,check_conf=True):
    cid = form.get('id', '')
    name = form.get('name', '')
    ids = form.getlist("ids")
    search_params = form.getlist("search_params")
    data = {}
    msg = []
    if cid:
        data['id'] = cid
    if name.strip():
        data['name'] = name.strip()
    else:
        msg.append(u"未配置报表名")
    if ids:
        data['cids'] = json.dumps([item for item in ids])
    else:
        msg.append(u"未选择报表")
    if search_params:
        data['globals'] = json.dumps([item.replace("&quot;","\"") for item in search_params])
    else:
        data['globals'] = ""
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
def get_chart(did,customs={},istable=False):
    if did:
        dinfo = dashboard_b.get_data_by_id(did)
        dinfo['cids'] = json.loads(dinfo['cids'])
        tmp_muti = {}
        global_customs = {}
        if u"0" in customs:
            global_customs = customs[u"0"]
        for item in dinfo['cids']:
            try:
                item = int(item)
                customs_split = {}
                if str(item) in customs:
                    customs_split = customs[str(item)]
                istable = global_customs['istable'] if "istable" in global_customs else customs_split.get('istable',False) or istable
                offset = global_customs['offset'] if "offset" in global_customs else customs_split.get('offset',0)
                length = global_customs['length'] if "length" in global_customs else customs_split.get('length',0)
                customs_conbine = conbine_customs(customs_split.get('customs',[]),global_customs.get("customs",[]))
                tmp_muti[item] = gevent.spawn(chart_m.get_chart,str(item),customs_conbine,istable,offset=offset,length=length)
            except Exception, e:
                pass
            
        gevent.joinall(tmp_muti.values())
        data = []
        msg = []
        for item in dinfo['cids']:
            try:
                item = int(item)
                if item in tmp_muti:
                    p = tmp_muti[item].value
                    if p:
                        data.append(p)
                    else:
                        msg.append(u"报表id为\"{}\"的数据返回错误，程序运行中断".format(item))
            except Exception, e:
                if ":" in item:
                    item = item.strip()
                    [name,iframe] = item.split(":",1)
                    # iframe=iframe.replace("\'","\\'")
                    iframe=iframe.replace("\'","&rsquo;")
                    tmp = {"status":1,"msg":""}
                    tmp['data'] = json.dumps({"url":iframe,"name":name},default=defaultencode)
                    tmp['chart_type'] = -1
                    data.append(tmp)
            
        if msg:
            result = {'status':0,'msg':";".join(msg)}
        else:
            search = parse_globals_tpl(dinfo['globals'],global_customs.get("0",{}))
            result = {"status":1,'msg':'',"search":search,'data':json.dumps(data,default=defaultencode)}
    else:
        result = {'status':0,'msg':u'dashboard id错误'}
    return result

#解析全局参数到模板
def parse_globals_tpl(params,globals_customs={}):
    result = []
    if params:
        globals_customs = globals_customs.get("customs","")
        globals_customs = parse_customs(globals_customs)
        params = json.loads(params)
        rows = []
        for item in params:
            item = json.loads(item)
            customs = item['globals']
            tmp = []
            tmp.append({"dtype":"label","content":item['params_customs_name'],"rowNum":1})
            t = {}
            item['params_types'] = int(item['params_types'])
            t['name'] = item['params_customs_name']
            t['rowNum'] = 2
            if item['params_customs_name'] in globals_customs:
                value = globals_customs[item['params_customs_name']]
            else:
                value = customs.get("params_default","")
            if item['params_types'] == 0:
                t['dtype'] = "input"
                t['value'] = value
            elif item['params_types'] == 1:
                t['dtype'] = "select"
                if customs['params_counts'].strip():
                    try:
                        customs['params_counts'] = int(customs['params_counts'])
                    except Exception, e:
                        customs['params_counts'] = 1
                else:
                    customs['params_counts'] = 1
                if customs['params_counts'] > 1:
                    t['dataLimit'] = customs['params_counts']
                    t['multiple'] = "multiple"
                    t['class'] = 'select2-multiple'
                    selected = customs.get("params_default","")
                    selected = selected.split(",")
                    selected = [item.strip("\"") for item in selected]
                    t['selected'] = selected if selected else ""
                    t['option'] = parse_options(customs.get("params_datasource",""))
                else:
                    t['class'] = 'select2-single'
                    t['selected'] = value
                    t['option'] = parse_options(customs.get("params_datasource",""))
            else:
                t = {}
                tmp = []
            if t:
                tmp.append(t)
            if tmp:
                rows.extend(tmp)
        result = [rows[i:i+4] for i in xrange(0,len(rows),4)]
        search_format = []
        search_format.append({"dtype":"label","content":"","rowNum":11})
        search_format.append({"dtype":"button","class":"btn-success submit","content":"search","rowNum":1})
        result.append(search_format)
    return result
def parse_options(customs):
    result = []
    if customs:
        customs = customs.strip().strip(";")
        data = []
        if customs.startswith("mysql://"):
            customs = customs.split(";",1)
            if len(customs) == 2:
                columns = mysql_base.get_data_mysql_columns(customs[0],customs[1],"")
                run_data = mysql_base.get_data_mysql(customs[0],customs[1],"")
                for item in run_data:
                    t = []
                    for it in columns:
                        t.append(str(item[it]))
                    data.append(t)
        else:
            data = customs.split(";",1)
            data = [item.split(":") for item in data]
        for item in data:
            if len(item) == 2:
                result.append({"value":item[1],"content":item[0]})
    return result

def parse_customs(string):
    result = {}
    if string.strip():
        string = string.split(";")
        for item in string:
            str_tmp = item.split(":",1)
            if len(str_tmp)==2:
                result[str_tmp[0].strip()] = str_tmp[1].strip()
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
