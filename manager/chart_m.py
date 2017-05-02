# -*- coding: utf-8 -*-
from base import chart_b,datasource_b
from common import utils
import json
from common.utils import defaultencode,muti_data_trans
from gevent import monkey; monkey.patch_all()
import gevent
import datasource_m
import cgi
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#获取数据源列表，增加了整体json编码
def get_datasource_list():
    datasources = datasource_b.get_datasource_list()
    result = []
    for item in datasources:
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
        data['customs'] = json.dumps(data['customs'])
        if 'id' in data and data['id']:
            result = chart_b.update(data)
        else:
            result = chart_b.save(data)
        return {'status':1,'msg':u'保存成功','data':result}
        try:
            pass
        except Exception, e:
            return {'status':0,'msg':u'保存失败，请先检查是否名称重复，如不重复联系管理员'}
#获取编辑页内容
def get_edit(sid):
    result = []
    if sid:
        data = chart_b.get_data_by_id(sid)
        if data:
            data['customs'] = json.loads(data['customs'])
            if data['customs']:
                conf = get_chart(sid,data['customs'])
                if conf['status'] == 1:
                    data['conf'] = conf['data']
                else:
                    data['conf'] = []
                keys = []
                tmp = []
                for item in data['customs']:
                    keys.extend(item.keys())
                if keys:
                    source_data = datasource_b.get_data_by_ids(keys)
                    source_data = utils.dbFormatToDict(source_data,"id")
                    if source_data:
                        for item in data['customs']:
                            tmp_dict = {}
                            for it in item:
                                it_k = int(it)
                                tmp_dict['customs'] = item[it]
                                tmp_dict['id'] = it
                                if it_k in source_data :
                                    tmp_dict['conf'] = source_data[it_k]
                                    tmp_dict['json'] = json.dumps(source_data[it_k],default=defaultencode)
                                    tmp_dict['json'] = cgi.escape(tmp_dict['json'],True)
                                else:
                                    tmp_dict['conf'] = None
                                    tmp_dict['json'] = None
                                tmp.append(tmp_dict)
                                break
                data['customs'] = tmp
            result = data
    return result

#解析参数
def parse_params(form,check_conf=True):
    cid = form.get('id', '')
    conf = form.get('conf', '')
    name = form.get('name', '')
    code = form.get('code','')
    customs = form.getlist("customs")
    ids = form.getlist("ids")
    data = {}
    msg = []
    if cid:
        data['id'] = cid
    if check_conf:
        if conf.strip():
            data['conf'] = conf
        else:
            msg.append(u"未配置报表图")
    if name.strip():
        data['name'] = name.strip()
    else:
        msg.append(u"未配置报表名")
    if ids:
        data['customs'] = []
        for key,item in enumerate(ids):
            data['customs'].append({item : customs[key]})
    else:
        msg.append(u"数据源为空,请至少选择一个数据源")
    if code.strip():
        data['code'] = code.strip()
    else:
        if len(ids)>1:
            msg.append("数据源大于1个，需要定义代码聚合数据")
        else:
            data['code'] = ''
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

#获取数据
def get_data(data,source_data,istestcode=False):
    source_data = utils.dbFormatToDict(source_data,"id")
    if source_data:
        tmp_source = 0
        tmp_muti = {}
        for item in data['customs']:
            tmp_dict = {}
            for it in item:
                it_k = int(it)
                if it_k in source_data and (not tmp_source):
                    conf = json.loads(source_data[it_k]['conf'])
                    conf = dict(source_data[it_k],**conf)
                    tmp_muti[it] = gevent.spawn(datasource_m.get_data,conf,item[it],istable=False)
                else:
                    tmp_source += 1
                break
        if tmp_source:
            tmp = []
            result = {'status':0,'msg':u'您选择的{}个数据源已下线,请重新选择'.format(tmp_source)}
        else:
            gevent.joinall(tmp_muti.values())
            tmp = []
            msg = []
            for item in data['customs']:
                for it in item:
                    if it in tmp_muti:
                        p = tmp_muti[it].value
                        if p:
                            if p['status'] == 1:
                                tmp.append(p['data'])
                            else:
                                msg.append(u"\"{}\"数据返回错误，错误信息为{}".format(source_data[int(it)]['name'],p['msg']))
                        else:
                            msg.append(u"\"{}\"数据返回错误，此数据源对应类型处理代码错误".format(source_data[int(it)]['name']))           
            if tmp:
                if msg:
                    result = {'status':0,'msg':";".join(msg)}
                else:
                    if istestcode:
                        tmp_data = []
                        for item in tmp:
                            tmp_data.append(utils.to_table(item))
                        result = {'status':1,'msg':u'','data':tmp_data}
                    else:
                        tmp_data = muti_data_trans(tmp,data['code'])
                        if tmp_data:
                            result = {'status':1,'msg':u'','data':tmp_data}
                        else:
                            result = {'status':0,'msg':u'代码有误，无法正常获取数据'}
            else:
                if msg:
                    result = {'status':0,'msg':";".join(msg)}
                else:
                    result = {'status':0,'msg':u'获取数据失败'}
    else:
        result = {'status':0,'msg':u'所有数据源均下线'}
    return result

#获取json的配置数据
def get_chart(sid,old_data=[],istable=False):
    if sid or old_data:
        data = chart_b.get_data_by_id(sid)
        tmp_data = {}
        for item in old_data:
            for it in item:
                tmp_data[it] = item[it]
        if data:
            if type(data['customs']) != list:
                data['customs'] = json.loads(data['customs'])
            keys = []
            for item in data['customs']:
                for it in item:
                    if it in tmp_data:
                        item[it] = tmp_data[it]
                keys.extend(item.keys())
            if keys:
                source_data = datasource_b.get_data_by_ids(keys)
                table_data = get_data(data,source_data)
                if table_data['status'] == 1:
                    if istable:
                        chart_conf = table_data['data']
                    else:
                        chart_conf = chart_b.get_chart(json.loads(data['conf']),table_data['data'])
                    result = {'status':1,'msg':u'','data':json.dumps(chart_conf,default=defaultencode)} 
                else:
                    result = table_data
            else:
                result = {'status':0,'msg':u'无数据源，请添加'}
        else:
            result = {'status':0,'msg':u'此图表已删除'}
    else:
        result = {'status':0,'msg':u'图表id错误'}    
    return result

def get_chart_customs(sid,customs=""):
    result = get_chart(sid)
    return result

#获取数据源列表
def get_list(sid="",name="",current=1,rowCount=20):
    data = chart_b.get_chart_list(sid,name,current=current,rowCount=rowCount)
    result = {}
    result['current'] = current
    result['rowCount'] = rowCount
    result['rows'] = []
    result['total'] = 0
    if data:
        for item in data:
            result['rows'].append(item)
        result['total'] = chart_b.get_chart_list(sid,name,iscount=True,current=current,rowCount=rowCount)
        return result
    return result
