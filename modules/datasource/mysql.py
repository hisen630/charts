# -*- coding: utf-8 -*-
from modules import DataSource
import json
from common import mysql_base,utils

class Manager(DataSource):
    """DataSource for Mysql"""
    def __init__(self):
        DataSource.__init__(self)
        self.types = 0

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
            if 'mysql_connect' in form:
                if form['mysql_connect'].strip():
                    conf['mysql_connect'] = form['mysql_connect'].strip()
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

    #根据提交内容获取转换后的数据
    def get_data(self,form,new_customs,rows='',istable=True):
        result = {'status':0,'msg':u'必要配置为空'}
        mysql_connect = form['mysql_connect']
        sqls = form['sqls']
        code = form['code']
        customs = form.get('customs',"")
        if new_customs:
            customs = mysql_base.combineCustom(customs,new_customs)
        if mysql_connect and sqls:
            check_result = mysql_base.check_conf(mysql_connect,sqls,code,customs)
            if check_result:
                result = check_result
            else:
                try:
                    data = mysql_base.get_data_mysql(mysql_connect,sqls,customs)
                    columns_names = mysql_base.get_data_mysql_columns(mysql_connect,sqls,customs)
                except Exception, e:
                    return {'status':0,'msg':u'sql 执行错误，请检查数据库连接和sql是否正确'}
                if data:
                    tmp = utils.data_trans(data,columns_names,code,istable)
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
                    result = {'status':0,'msg':u'数据为空'}
        return result

    #检查创建notebook时参数是否正确
    def check_notebook_params(self,form):
        result = {'status':0,'msg':u'必要配置为空，请填写'}
        mysql_connect = form.get("mysql_connect","")
        sqls = form.get("sqls","")
        code = form.get("code","")
        customs = form.get("customs","")
        if mysql_connect and sqls:
            check_result = mysql_base.check_conf(mysql_connect,sqls,code,customs)
            if check_result:
                result = check_result
            else:
                [now_sql,customs] = mysql_base.parse_sql(sqls,customs)
                sqls = now_sql
                try:
                    data = mysql_base.get_data_mysql(mysql_connect,sqls,customs)
                except Exception, e:
                    return {'status':0,'msg':u'sql 执行错误，请检查数据库连接和sql是否正确'}
                return {'status':1,'msg':u''}
        return result

    #生成notebook代码
    def create_notebook_code(self,form,path=""):
        tmp = []
        db_connect = mysql_base.parse_mysql(form['mysql_connect'])
        [now_sql,customs] = mysql_base.parse_sql(form['sqls'],form['customs'])
        tmp.append(r'''db=dbs.create_engine_custom(dbn="{}",db="{}",host="{}",port={},user="{}",pw="{}")'''.format(
            db_connect['ENGINE'],db_connect['NAME'],db_connect['HOST'],db_connect['PORT'],db_connect['USER'],db_connect['PASSWORD']))
        tmp.append(r'''sqls=r"""{}"""'''.format(now_sql))
        tmp.append(r'''result=db.query(sqls)''')
        tmp.append(r'''columns_names=db.columns_name(sqls)''')
        tmp.append(r'''result=DataFrame([x for x in result],columns=columns_names)''')
        tmp.append(r'result[:2]')
        print tmp
        return {'status':1,"msg":'','data':tmp}
