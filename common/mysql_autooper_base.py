# -*- coding: utf-8 -*-
from hillinsight.storage.db_conn import _mysql_config
import re
import datetime
from conf.default import _time_column
import hashlib
_md5_sum = hashlib.md5() 

_match = re.compile(r";$")

class AutoOper():
    #参数初始化
    def __init__(self):
        self.db = "god_metric"
        self.relation_db = "god_metric_meta"
        self.master = _mysql_config[self.db]['master']['offline']
        self.slave = _mysql_config[self.db]['slave']['offline']
        self.relation_table = "t_chart_task_relation"
        self.relation = _mysql_config[self.relation_db]['master']['offline']
        #table,column,key
        self.sql = u'''CREATE TABLE if not exists `{}` ( `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键', {} `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',PRIMARY KEY (`id`) {} ) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
        #type,id,date,autoid
        self.table = "t_task_{}_{}_{}_{}"

    #更新数据
    def _replace_data(self,date,data,table):
        result = {'status':0,'msg':u'auto oper 数据为空'}
        if data:
            try:
                self.master.query("delete from {} where {}='{}'".format(table,_time_column,date))
                self.master.multiple_replace(table,data)
                result = {'status':1,'msg':u''}
            except Exception, e:
                result = {'status':0,'msg':u'auto oper 保存至数据库失败{}'.format(e)}
        return result

    #创建数据库表sql
    def _create_table_sql(self,types,ids,header,data,date,table_tag='1',keys=[],u_k=[]):
        result = {'status':0,'msg':u'auto oper 数据为空'}
        if data:
            tmp_data = data[0]
            columns = {}
            for item in header:
                is_num = self._is_num(tmp_data[item])
                if is_num:
                    columns[item] = is_num
                else:
                    columns[item] = type(tmp_data[item])
            columns = self._create_columns(columns)
            if columns:
                columns_str = []
                for item in header:
                    columns_str.append(columns[item])
                columns_str = "{} ,".format(",".join(columns_str))
                _md5_sum.update(table_tag)
                table_suffix = _md5_sum.hexdigest()
                table = self.table.format(types,ids,date,table_suffix)
                keys = ",".join(self._create_key(keys,u_k))
                if keys:
                    keys = ", {} ".format(keys)
                sql = self.sql.format(table,columns_str,keys)
                result = {'status':1,'msg':u'','data':sql,'table':table}
            else:
                result = {'status':0,'msg':u'auto oper 包含非法数据类型，正常为数字类型和字符串类型,或者无字段'}
        return result

    #在库中生成数据表
    def _create_table(self,types,ids,header,data,date,table_tag="1",keys=[],u_k=[]):
        sql_result = self._create_table_sql(types,ids,header,data,date,table_tag,keys,u_k)
        if sql_result['status'] == 0:
            return sql_result
        else:
            sql = sql_result['data']
            try:
                self.master.query(sql)
                result = {'status':1,'msg':u'','table':sql_result['table']}
            except Exception, e:
                result = {'status':0,'msg':u'auto oper 创建数据表到数据库失败{}'.format(e)}
            return result

    #判断int还是float还是字符串类型
    def _is_num(self,data):
        try:
            t = float(data)
            if type(eval(data)) == int:
                return int
            elif type(eval(data)) == float:
                return float
        except Exception, e:
            pass
        return False

    #转换数据类型到单一类型
    def _create_columns(self,columns):
        result = {}
        if columns:
            for item in columns:
                if columns[item] in (int,float,bool,long):
                    result[item] = r"`{}` DECIMAL(64,2) NULL DEFAULT NULL".format(item.strip())
                elif columns[item] in (object,tuple,list,dict,set):
                    return False
                elif columns[item] == datetime.date:
                    result[item] = r"`{}` date NULL DEFAULT NULL".format(item.strip())
                elif item == _time_column:
                    result[item] = r"`{}` TIMESTAMP NULL DEFAULT NULL".format(item.strip())
                else:
                    result[item] = r"`{}` varchar(200) NULL DEFAULT NULL".format(item.strip())
        return result

    #转换数据类型到单一类型
    def _create_key(self,keys=[],u_ks=[]):
        result = []
        if keys:
            for item in keys:
                if item and type(item) == list:
                    key_name = "_".join(item)
                    key_column = "`,`".join(item)
                    result.append(" INDEX `{}` (`{}`) ".format(key_name,key_column))
        if u_ks:
            for item in u_ks:
                if item and type(item) == list:
                    key_name = "_".join(item)
                    key_column = "`,`".join(item)
                    result.append(" UNIQUE INDEX `{}` (`{}`) ".format(key_name,key_column))
        return result 

    #写入关系表以便后期查询
    def _write_relation(self,ids,table,date,table_tag):
        result = {'status':0,'msg':u'auto oper 写入数据库关系失败'}
        if ids:
            form = {}
            form['tid'] = ids
            form['tables'] = table
            form['date'] = date
            form['table_tag'] = table_tag
            try:
                self.relation.replace(self.relation_table,**form)
                result = {'status':1,'msg':u''}
            except Exception, e:
                result = {'status':0,'msg':u'auto oper 写入数据库关系失败 {}'.format(e)}
        return result

    #获取所有数据表
    def _get_table_by_id(self,ids,tid_table=""):
        result =[]
        where = ""
        if tid_table:
            where = " and id={} ".format(tid_table)
        if ids:
            result = self.relation.query("select * from {} where tid={} {};".format(self.relation_table,ids,where))
        return result

    #执行sql查询
    def _get_data_by_sql(self,sql):
        return self.master.query(sql)

    #执行sql查询
    def _get_columns_by_sql(self,sql):
        return self.master.columns_name(sql)

    #写入数据库
    def write_data(self,ids,types,header,data,date,table_tag="1",key=[],u_k=[]):
        result = {'status':0,'msg':u'auto oper 数据为空'}
        table_date = date[:10].replace("-","")
        if header and data:
            tmp_result = self._create_table(ids,types,header,data,table_date[:6],table_tag,key,u_k)
            if tmp_result['status'] == 1:
                table = tmp_result['table']
                try:
                    tmp_result = self._write_relation(ids,table,table_date,table_tag)
                except Exception, e:
                    tmp_result = {'status':0,'msg':u'auto oper 写入关系表数据库代码有误'}
                if tmp_result['status'] == 1:
                    tmp_result = self._replace_data(date,data,table)
                    result = tmp_result
                else:
                    result = tmp_result
            else:
                result = tmp_result
        return result

    #从数据库读取
    def read_data(self,ids,sqls,tid_table=""):
        result = {'status':0,'msg':u'auto oper 根据id获取数据失败'}
        if ids:
            tables = self._get_table_by_id(ids,tid_table)
            if tables:
                sqls = _match.sub(" ",sqls.strip())
                if "task_table" in sqls:
                    fininal_sql = []
                    for item in tables:
                        tmp_sql = sqls
                        tmp_sql = tmp_sql.replace("task_table",item['tables'])
                        fininal_sql.append("({})".format(tmp_sql))
                    fininal_sql = " union ".join(fininal_sql)
                    try:
                        data = self._get_data_by_sql(fininal_sql)
                        columns = self._get_columns_by_sql(fininal_sql)
                        result = {'status':1,'msg':u'','data':data, 'columns':columns}
                    except Exception, e:
                        result = {'status':0,'msg':u'auto oper sql执行错误，请检查'}
                else:
                    result = {'status':0,'msg':u'auto oper sql没按照格式要求将表名写成task_table'}
            else:
                result = {'status':1,'msg':u'auto oper 无此id对应的表数据','data':[]}
        return result
    def del_data(self,ids,where):
        result = {'status':0,'msg':'删除时缺少where语句'}
        if ids and where:
            tables = self._get_table_by_id(ids)
            if tables:
                sql = "delete from {} where {}"
                for item in tables:
                    try:
                        self.master.query(sql.format(item['tables'],where))
                    except Exception, e:
                        return {'status':0,'msg':u'执行删除语句失败'}
            result = {'status':1,'msg':''}
        return result
