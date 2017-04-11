# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from base import notebook_b
from common import mysql_base
from common.utils import defaultencode
import datasource_m,chart_m
from common.base import get_module_object
from conf.default import _notebook_path

_header = [u'#运行如下语句进行数据准备','import web',r'%matplotlib inline',r'%pylab inline','from pandas import DataFrame,Series',
        'import pandas as pd;import numpy as np','from hillinsight.storage import dbs']

def get_notebook(form):
    result = {'status':0,'msg':u'必要配置为空，请填写'}
    types = form.get("types","-1")
    types = int(types)
    module_type = form.get("module_type","datasource")
    objects = get_module_object(module_type)

    for item in objects:
        if objects[item].types == types:
            result = objects[item].check_notebook_params(form)
    code = []
    name = notebook_b.new_notebook()
    if name:
        path = '{}/{}.data_tmp'.format(_notebook_path,name)
        if result['status'] == 1:
            for item in objects:
                if objects[item].types == types:
                    code_result = objects[item].create_notebook_code(form,path=path)
                    if code_result['status'] == 0:
                        return code_result
                    else:
                        code = code_result['data']
        codes = list(_header)
        codes.extend(code)
        temp = notebook_b.init_notebook(name,codes,form['code'])
        if temp:
            return {'status':1,'msg':u'','data':temp}
        else:
            return {'status':0,'msg':u'初始化notebook失败，请重试'}
    else:
        result = {'status':0,'msg':u'创建notebook失败，请重试'}
    return result

def get_notebook_muti(form):
    data = chart_m.get_data_by_form(form,True)
    data = json.dumps(data,default=defaultencode)
    name = notebook_b.new_notebook()
    path = '{}{}.data_tmp'.format(_notebook_path,name)
    try:
        file_object = open(path, 'wb')
        file_object.write(data)
        file_object.close()
    except Exception, e:
        return {'status':0,'msg':u'数据写入文件失败，{}'.format(e)}
    code = u"""import json\npath="{}"\nrecords = [json.loads(item) for item in open(path)][0]['data']\nresult = []\nfor item in records:\n    columns = item[0]\n    data = item[1:]\n    result.append(DataFrame(data,columns=columns))\nresult[0][:2]""".format(path)
    codes = list(_header)
    codes.extend([code])
    customs_code = "def trans(args):\n    return args[0]"
    if form['code'].strip():
        customs_code = form['code']
    temp = notebook_b.init_notebook(name,codes,customs_code)
    if temp:
        return {'status':1,'msg':u'','data':temp}
    else:
        return {'status':0,'msg':u'初始化notebook失败，请重试'}
