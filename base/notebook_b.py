# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from common.utils import _req_url_body
from common import mysql_base
from conf.default import NOTEBOOK_URL

'''init notebook default params '''
def init_notebook(name,first=[],code=""):
    result = []
    if first:
        result.append("\n".join(first))
    #自定义trans
    if code:
        result.append(code)
    else:
        tmp = ['def trans(frame):']
        tmp.append('    return frame')
        result.append("\n".join(tmp))
    #运行查看内容
    result.append("trans_data = trans(result)\ntrans_data[:5]")
    result.append("def to_table(frame):\n    columns = frame.columns\n    indexs = frame.index\n    if indexs.name:\n        header = [indexs.name]+columns.values.tolist()\n    else:\n        header = columns.values.tolist()\n    indexs_list = frame.index.values.tolist()\n    data = np.array(frame).tolist()\n    if indexs.name:\n        tmp = [item.insert(0,indexs_list[key]) for key,item in enumerate(data)]\n    data.insert(0,header)\n    return data\ntmp = to_table(trans_data)\ntmp[:5]")
    data_jsons = r''' {"type":"notebook","content":{"cells":[{"metadata":{"trusted":true,"collapsed":true},"cell_type":"code","source":"#运行如下三句以进行数据准备\nsql_statment = \"select ...\"\nimport MySQLdb\nconn = ...\nresult = DataFrame(mysql.query(sql))","execution_count":null,"outputs":[]}],"metadata":{"kernelspec":{"name":"python2","display_name":"Python 2","language":"python"},"language_info":{"mimetype":"text/x-python","nbconvert_exporter":"python","name":"python","pygments_lexer":"ipython2","version":"2.7.12","file_extension":".py","codemirror_mode":{"version":2,"name":"ipython"}}},"nbformat":4,"nbformat_minor":0}} '''
    data_jsons = json.loads(data_jsons)
    cells = data_jsons['content']['cells']
    temp = dict(cells[0])
    cells = []
    for item in result:
        tmp = dict(temp)
        tmp['source'] = item
        cells.append(tmp)
    data_jsons['content']['cells'] = cells
    url = "{}/api/contents/{}".format(NOTEBOOK_URL,name)
    try:
        result = _req_url_body(url,data_jsons,True)
        result = json.loads(result)
        if result['writable']:
            return "{}/notebooks/{}".format(NOTEBOOK_URL,name)
    except Exception, e:
        return False

'''create a new notebook'''
def new_notebook():
    url = "{}/api/contents".format(NOTEBOOK_URL)
    data = {"type":"notebook"}
    try:
        result = _req_url_body(url,data)
        result = json.loads(result)
        return result['name']
    except Exception, e:
        return False
