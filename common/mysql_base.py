# -*- coding: utf-8 -*-
from hillinsight.storage import dbs
from dj_database_url import parse as parse_db_url
from time_base import get_time
import time
from utils import _req_url_body
_format = {
    'Y':"%Y",
    "m":"%m",
    "d":"%d",
    "H":"%H",
    "M":"%M",
    "S":"%S",
    "s":""
}

_format_time = r'%Y-%m-%d %H:%M:%S'

def check_conf(mysql_connect='',sqls='',code='',custom=''):
    result = {}
    if mysql_connect:
        try:
            db = parse_mysql(mysql_connect)
        except Exception, e:
            result['status'] = 0
            result['msg'] = u'mysql连接配置有误'
            return result
    if sqls:
        # try:
        [sqls,custom] = parse_sql(sqls,custom)
        # except Exception, e:
        #     result['status'] = 0
        #     result['msg'] = u'sql配置有误'
        #     return result
    if code:
        try:
            code = code
        except Exception, e:
            result['status'] = 0
            result['msg'] = u'字段名错误'
            return result
    return result

def get_sql(sqls,custom='',attach=''):
    result = {'status':0,'msg':u'获取失败'}
    if sqls:
        check_result = check_conf(sqls=sqls,custom=custom)
        if check_result:
            result = check_result
        else:
            [data,custom] = parse_sql(sqls,custom)
            attach = attach.strip()
            if attach and not attach[-1] == ";":
                attach = "{};".format(attach)
            data = "{}{}".format(attach,data)
            result = {'status':1,'msg':u'获取成功','data':data}
    else:
        result = {'status':0,'msg':u'sql为空'}
    return result

def parse_mysql(mysql_connect):
    if mysql_connect:
        mysql = parse_db_url(mysql_connect,"mysql")
        if mysql['HOST'] and mysql['ENGINE'] and mysql['PASSWORD'] and mysql['USER']:
            if not mysql['PORT']:
                mysql['PORT'] = 3306
            return mysql
    raise Exception("mysql config error","conf_error")

def parse_sql(sql,custom,timestramp=0):
    if custom:
        if type(custom) != list:
            custom = custom.split(";")
        customs = {}
        customs_old = {}
        for item in custom:
            tmp = item.split(":",1)
            tmp_len = len(tmp)
            for x in xrange(0,tmp_len):
                tmp[x] = tmp[x].strip('''"\'''').strip()
            if "#" not in tmp[0]:
                continue
            if tmp_len == 2:
                customs_old[tmp[0]] = tmp[1]
                if 'now' in tmp[1]:
                    tmp[1] = get_time(tmp[1],timestramp)
                customs[tmp[0]] = tmp[1]
            elif tmp_len == 1:
                customs[tmp[0]] = ""
                customs_old[tmp[0]] = ""
            else:
                continue
        if customs:
            tmp = []
            for item in customs:
                sql = sql.replace(item,customs[item])
                tmp.append(u"{}:{}".format(item,customs_old[item]))
            custom = ";".join(tmp)
    return [sql,custom]

def get_data_mysql(mysql_connect,sql,custom,timestramp=0):
    [sql,custom] = parse_sql(sql,custom,timestramp)
    db = parse_mysql(mysql_connect)
    db = dbs.create_engine_custom(dbn=db['ENGINE'],db=db['NAME'],host=db['HOST'],port=db['PORT'],user=db['USER'],pw=db['PASSWORD'])
    data = db.query(sql)
    db.ctx.db.close()
    return data

def get_data_mysql_columns(mysql_connect,sql,custom):
    [sql,custom] = parse_sql(sql,custom)
    db = parse_mysql(mysql_connect)
    db = dbs.create_engine_custom(dbn=db['ENGINE'],db=db['NAME'],host=db['HOST'],port=db['PORT'],user=db['USER'],pw=db['PASSWORD'])
    data = db.columns_name(sql)
    db.ctx.db.close()
    return data

def combineCustom(old,new):
    if new:
        #提取旧custom内容
        old = old.split(";")
        tmp_old = {}
        for item in old:
            tmp = item.split(":",1)
            tmp_len = len(tmp)
            for x in xrange(0,tmp_len):
                tmp[x] = tmp[x].strip('''"\'''').strip()
            if "#" not in tmp[0]:
                continue
            if tmp_len == 2:
                tmp_old[tmp[0]] = tmp[1]
            elif tmp_len == 1:
                tmp_old[tmp[0]] = ""
            else:
                continue
        #提取新custom内容
        new = new.split(";")
        tmp_new = {}
        for item in new:
            tmp = item.split(":",1)
            tmp_len = len(tmp)
            for x in xrange(0,tmp_len):
                tmp[x] = tmp[x].strip('''"\'''').strip()
            if "#" not in tmp[0]:
                continue
            if tmp_len == 2:
                tmp_new[tmp[0]] = tmp[1]
            elif tmp_len == 1:
                tmp_new[tmp[0]] = ""
            else:
                continue
        for item in tmp_new:
            if item in tmp_old:
                tmp_old[item] = tmp_new[item]
        if tmp_old:
            old = []
            for item in tmp_old:
                old.append("{}:{}".format(item,tmp_old[item]))
            old = ";".join(old)
    return old
