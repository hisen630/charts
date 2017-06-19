# -*- coding: utf-8 -*-
from hillinsight.storage import dbs
from dj_database_url import parse as parse_db_url
from conf import hive as _hive
from conf.default import HIVE_IS_HAVE_DBS
import hql_profile_base
import datetime
import os
from utils import _req_url_body
import hashlib
import random
import commands
_md5_sum = hashlib.md5()

#parse fakecube params from hql
def get_profile(sqls):
    return hql_profile_base.profile_from_hql(sqls)

#get the result by run the fakecube
def get_data_hive(sqls,profile={},is_hive=False):
    result = {"status":0,"msg":u"hive执行失败"}
    if not os.path.exists(_hive.TMP_SQL_PATH):
        os.mkdir(_hive.TMP_SQL_PATH)
    if not os.path.exists(_hive.TMP_DATA_PATH):
        os.mkdir(_hive.TMP_DATA_PATH)
    if not os.path.exists(_hive.TMP_LOG_PATH):
        os.mkdir(_hive.TMP_LOG_PATH)
    _md5_sum.update("{}{}{}".format(sqls,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"),random.random()))
    filename = "{}/{}.data".format(_hive.TMP_DATA_PATH,_md5_sum.hexdigest())
    sql_filename = "{}/{}.sql".format(_hive.TMP_SQL_PATH,_md5_sum.hexdigest())
    log_file = "{}/{}.log".format(_hive.TMP_LOG_PATH,_md5_sum.hexdigest())
    #run fakecube and put the data to file
    if is_hive:
        sqls = "{}{}".format("set hive.cli.print.header=true;",sqls)
    exe_result = excute_sqls(sqls,sql_filename,filename,log_file)
    if exe_result['status'] == 0:
        return exe_result
    #read data from file and split the data by grouping_set
    if is_hive:
        exe_result = readfile_to_group_hive(filename)
    else:
        exe_result = readfile_to_group_fakecube(filename,profile)
    if exe_result['status'] == 0:
        return exe_result
    return exe_result

#put the data to file
def excute_sqls(sqls,sql_filename,filename,log_file,attach=""):
    result = {'status':0,"msg":""}
    if attach !='':
        ending = attach[-1]
        if ending != ';':
            attach +=';'
        sqls = '%s %s' % (attach, sqls)
    with open(sql_filename,'w') as f:
        f.write(sqls)

    cmd = "hive -f {} >{} 2>>{}".format(sql_filename,filename,log_file)
    retu=os.system(cmd)
    os.remove(sql_filename)
    if retu==0:
        result['status'] = 1
    else:
        result['msg'] = u'命令执行失败，请检查hql是否正确'
    
    return result

#read data from file and split the data by grouping_set
def readfile_to_group_hive(filename):
    header = []
    c = 0
    header_len = 0
    result = {}
    for item in open(filename):
        line = item.split("\t")
        #防止出现换行符，如果出现无法插入数据
        line = [ it.strip() for it in line ]
        if c == 0:
            if not HIVE_IS_HAVE_DBS:
                #防止出现表名入test.test
                tmp_line = []
                for it in line:
                    tmp = it.split(".")
                    if len(tmp) > 1:
                        tmp = tmp[1:]
                    tmp_line.append(".".join(tmp))
                line = tmp_line
            c += 1
            header = line
            header_len = len(header)
        else:
            if len(line) ==  header_len:
                if "0" not in result:
                    result["0"] = {}
                    result["0"]['data'] = []
                    result["0"]['columns'] = header
                    result["0"]['dimensions'] = []
                result["0"]['data'].append(line)
            else:
                return {"status":0,"msg":u"hive执行失败,hive从文件解析数据失败,数据行与列数不匹配"}
    os.remove(filename)
    return {"status":1,"msg":u"",'data':result}

#read data from file and split the data by grouping_set
def readfile_to_group_fakecube(filename,profile):
    header = profile['dimensions'] + ['grouping__id'] + profile["metrics"]
    h_len = len(header)
    g_len = len(profile['dimensions'])
    group_id_dict = {}
    group_id_dict_select = {}
    p_len = len(profile['dimensions_in_select'])
    for key,it in enumerate(profile['dimensions']):
        group_id_dict[key] = it
    for key,it in enumerate(profile['dimensions_in_select']):
        group_id_dict_select[it] = key
    result = {}
    for item in open(filename):
        line = item.split("\t")
        #防止出现换行符，如果出现无法插入数据
        line = [ it.strip() for it in line ]
        if len(line) == h_len:
            g_id = line[g_len]
            if g_id not in result:
                #转义grouping_id到字段名称
                dimensions = []
                try:
                    g_id = int(g_id)
                    current = 0
                    while True:
                        if g_id == 0:
                            dimensions = profile['dimensions_in_select']
                            break
                        if g_id&1:
                            if current < g_len:
                                if group_id_dict[current] in profile['dimensions_in_select']:
                                    dimensions.append(group_id_dict[current])
                            else:
                                return {"status":0,"msg":u"hive执行失败,从文件解析到组失败,长度超过dimensions长度"}
                        if g_id == 1:
                            break
                        current += 1
                        g_id = g_id>>1

                except Exception, e:
                    return {"status":0,"msg":u"hive执行失败,从文件解析到组失败,组id解析失败：{}".format(g_id)}
            else:
                dimensions = result[g_id]['dimensions']
            #根据grouping_id组合字典
            tmp = []
            for key,it in enumerate(profile['dimensions_in_select']):
                if it in dimensions:
                    tmp.append(line[key])
            for key,it in enumerate(profile['metrics']):
                tmp.append(line[p_len+key])
            if line[g_len] not in result:
                result[line[g_len]] = {}
                result[line[g_len]]['data'] = []
                result[line[g_len]]['columns'] = dimensions + profile['metrics']
                result[line[g_len]]['dimensions'] = dimensions
            result[line[g_len]]['data'].append(tmp)
        else:
            return {"status":0,"msg":u"hive执行失败,从文件解析到组失败,数据行与列数不匹配"}
    os.remove(filename)
    return {"status":1,"msg":u"",'data':result}

