# -*- coding: utf-8 -*-
from modules import DataSource
import json
from common import mysql_base,utils
from base import task_b
from common.mysql_autooper_base import AutoOper
from common.utils import defaultencode

class Manager(DataSource):
    """DataSource for Mysql"""
    def __init__(self):
        DataSource.__init__(self)
        self.types = 1

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
            if 'code' in form:
                conf['code'] = form['code']
            if 'tid' in form:
                if form['tid']:
                    conf['tid'] = form['tid']
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
                else:
                    return return_result
            else:
                return return_result
            if 'customs' in form:
                if form['customs'].strip():
                    conf['customs'] = form['customs'].strip()
            else:
                return return_result
            check_result = mysql_base.check_conf(conf.get('mysql_connect',''),conf.get('sqls',""),conf.get('code',""),conf.get('custom',""))
            if check_result:
                return check_result
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

    def get_datasource_other(self,data):
        tasks = task_b.get_task_list(types=self.types,rowCount=0)
        data['tasks'] = []
        for item in tasks:
            data['tasks'].append(item)
        return data


    #根据提交内容获取转换后的数据
    def get_data(self,form,new_customs,rows='',istable=True,is_run_code=True):
        result = {'status':0,'msg':u'必要配置为空，请检查数据源和sql是否为空'}
        tid = form['tid']
        sqls = form['sqls']
        code = form['code']
        if not is_run_code:
            code = ""
        customs = form.get('customs',"")
        if new_customs:
            customs = mysql_base.combineCustom(customs,new_customs)
        if tid and sqls:
            check_result = mysql_base.check_conf("",sqls,code,customs)
            if check_result:
                result = check_result
            else:
                (sqls,customs) = mysql_base.parse_sql(sqls,customs)
                data_result = AutoOper().read_data(tid,sqls)
                try:
                    pass
                except Exception, e:
                    return {'status':0,'msg':u'sql 执行错误，请检查sql是否正确'}
                if data_result['status'] == 1:
                    tmp = utils.data_trans(data_result['data'],data_result.get('columns'),code,istable)
                    if istable:
                        if not tmp:
                            return {'status':0,'msg':u'数据为空或者自定义代码错误'}
                    else:
                        if tmp.empty:
                            return {'status':0,'msg':u'数据为空或者自定义代码错误'}
                    try:
                        if rows and int(rows):
                            tmp = tmp[:int(rows)]
                    except Exception, e:
                        tmp = tmp[:10]
                    
                    result = {'status':1,'msg':u'','data':tmp}
                else:
                    result = data_result
        return result

    #检查创建notebook时参数是否正确
    def check_notebook_params(self,form):
        result = {'status':0,'msg':u'必要配置为空，请填写'}
        tid = form['tid']
        sqls = form.get("sqls","")
        code = form.get("code","")
        customs = form.get("customs","")
        if tid and sqls:
            check_result = mysql_base.check_conf("",sqls,code,customs)
            if check_result:
                result = check_result
            else:
                [now_sql,customs] = mysql_base.parse_sql(sqls,customs)
                sqls = now_sql
                try:
                    data_result = AutoOper().read_data(tid,sqls)
                except Exception, e:
                    return {'status':0,'msg':u'sql 执行错误，请检查是否选择数据源或sql是否正确'}
                return {'status':1,'msg':u''}
        return result

    #生成notebook代码
    def create_notebook_code(self,form,path=""):
        data = self.get_data(form,"",is_run_code=False)
        data = json.dumps(data,default=defaultencode)
        try:
            file_object = open(path, 'wb')
            file_object.write(data)
            file_object.close()
        except Exception, e:
            return {'status':0,"msg":u'数据写入文件失败，{}'.format(e)}
        code = u"""import json\npath="{}"\nrecords = [json.loads(item) for item in open(path)][0]['data']\ncolumns = records[0]\ndata = records[1:]\nresult = DataFrame(data,columns=columns)\nresult[:2]""".format(path)
        return {'status':1,"msg":'','data':[code]}
