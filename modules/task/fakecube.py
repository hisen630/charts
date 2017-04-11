# -*- coding: utf-8 -*-
from modules import DataSource
import json
from common import mysql_base,utils,hive_base
from common.mysql_autooper_base import AutoOper
import time
from modules.datasource.mysql_caculate import Manager as ds_Manager
from conf.default import _time_column

class Manager(DataSource):
    """Task for Hive"""
    def __init__(self):
        DataSource.__init__(self)
        self.types = 2

    #转换为可保存的字典类型
    def save_dict(self,form):
        if form:
            return_result = {'status':0,'msg':'必要项为空'}
            result = {'types':self.types}
            conf = {}
            form = form.to_dict()
            if 'id' in form:
                if form['id']:
                    result['id'] = form['id']
                elif form['id'].strip() == '':
                    pass
                else:
                    return return_result
            if 'st' in form:
                if form['st'].strip():
                    result['st'] = form['st'].strip()
                else:
                    result['st'] = utils.get_time()
            else:
                result['st'] = utils.get_time()
            if 'et' in form:
                if form['et'].strip():
                    result['et'] = form['et'].strip()
                else:
                    result['et'] = utils.get_time(False)
            else:
                result['et'] = utils.get_time(False)
            if 'cron' in form:
                if form['cron'].strip():
                    result['cron'] = form['cron'].strip()
                else:
                    return return_result
            else:
                return return_result
            if 'name' in form:
                if form['name'].strip():
                    result['name'] = form['name'].strip()
                else:
                    return return_result
            else:
                return return_result
            if 'sqls' in form:
                if form['sqls'].strip():
                    conf['sqls'] = form['sqls'].strip()
                    conf['profile'] = self.get_data(form)
                    if conf['profile']['status'] == 0:
                        return conf['profile']
                    else:
                        conf['profile'] = conf['profile']['data']
                else:
                    return return_result
            else:
                return return_result
            conf['del_where'] = ""
            if 'del_where' in form:
                if form['del_where'].strip():
                    conf['del_where'] = form['del_where'].strip()
            conf['hql_params'] = ""
            if 'hql_params' in form:
                if form['hql_params'].strip():
                    conf['hql_params'] = form['hql_params'].strip()
            if 'customs' in form:
                if form['customs'].strip():
                    conf['customs'] = form['customs'].strip()
            else:
                return return_result
            result['conf'] = json.dumps(conf)
            return_result['status'] = 1
            return_result['data'] = result
        return return_result

    #提出配置，转换为字典，以便渲染
    def get_datasource(self,data):
        result = {}
        if data:
            data['conf'] = json.loads(data['conf'])
            result = dict(data,**data['conf'])
        return result

    #根据提交内容获取转换后的配置信息
    def get_data(self,form,new_customs='',rows='',istable=False):
        result = {'status':0,'msg':u'必要配置为空'}
        sqls = form['sqls']
        customs = form['customs']
        if new_customs:
            customs = mysql_base.combineCustom(customs,new_customs)
        sqls = mysql_base.parse_sql(sqls,customs)
        if sqls:
            try:
                status,data = hive_base.profile_from_hql(sqls)
                data = data.__dict__
            except Exception, e:
                return {'status':0,'msg':u'解析hql出错请检查是否正确'}
            result = {'status':1,'msg':u'','data':data}
        return result

    #根据提交内容获取转换后的数据信息
    def get_data_group(self,form,new_customs,timestramp):
        sqls = form['sqls']
        customs = form.get("customs","")
        profile = form.get("profile",{})
        hql_params = form.get("hql_params","")
        if new_customs:
            customs = mysql_base.combineCustom(customs,new_customs)
        [sqls,customs] = mysql_base.parse_sql(sqls,customs,timestramp)
        if sqls:
            try:
                hql_params = hql_params.strip()
                if hql_params and not hql_params[-1] == ";":
                    hql_params = "{};".format(hql_params)
                sqls = "{}{}".format(hql_params,sqls)
                data = hive_base.get_data_hive(sqls,profile)
            except Exception, e:
                return {'status':0,'msg':u'解析hql出错请检查是否正确'}
            if data['status']:
                return {'status':1,"data":data['data']}
            else:
                return data
        return {'status':0,'msg':u'必要配置为空'}

    #运行计划任务时使用
    def run_task(self,task,timestramp):
        result = {'status':0,'msg':u"类型错误"}
        if task['types'] == self.types:
            conf = json.loads(task['conf'])
            datas = self.get_data_group(conf,"",timestramp=timestramp)
            auto = AutoOper()
            if datas['status'] == 1:
                if conf['del_where']:
                    del_info = auto.del_data(task['id'],conf['del_where'])
                    if del_info['status'] == 0:
                        return del_info
                date = time.strftime("%Y-%m-%d %X",time.localtime(timestramp))
                for item in datas['data']:
                    tmp_data = datas['data'][item]['data']
                    tmp_data[:0] = [datas['data'][item]['columns']]
                    (header,data) = utils.to_dict(tmp_data,insert_header = [{_time_column:date}])
                    result = AutoOper().write_data(task['id'],self.types,header,data,date,
                        table_tag=",".join(datas['data'][item]['dimensions']),key=[[_time_column],datas['data'][item]['dimensions']])
            else:
                result = datas
        return result
