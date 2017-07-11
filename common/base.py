# -*- coding: utf-8 -*-
import numpy as np
from json import dumps
from manager import menu_m
from utils import get_py_file
from common.logger import logger
from web.utils import IterBetter
from traceback import format_exc
from pandas import DataFrame, Series
from conf.default import MODULES_NAME
from flask import request, render_template as render

'''get modules from python file'''


def get_module_object(_modules_split, modules=MODULES_NAME):
    objects = {}
    files = get_py_file("{}/{}/*".format(modules, _modules_split))
    for it in files:
        try:
            tmp = __import__('{}.{}.{}'.format(modules, _modules_split, it), globals(), locals(), [it])
            objects[it] = tmp.Manager()
        except Exception, e:
            logger.warning(format_exc())
    return objects


'''add menus to render'''


def render_custom(tpl, **args):
    menus = menu_m.get_menus(request.url)
    return render(tpl, menus=menus, **args)


def to_table(frame):
    columns = frame.columns
    indexs = frame.index
    tmp_columns = columns.values.tolist()

    if indexs.name:
        if type(tmp_columns) in (list, tuple):
            header = [indexs.name] + ["_".join(item) for item in tmp_columns]
        else:
            header = [indexs.name] + tmp_columns
    else:
        if type(tmp_columns) in (list, tuple):
            header = ["_".join(item) for item in tmp_columns]
        else:
            header = tmp_columns
    indexs_list = frame.index.values.tolist()
    data = np.array(frame).tolist()
    if indexs.name:
        tmp = [item.insert(0, indexs_list[key]) for key, item in enumerate(data)]
    data.insert(0, header)
    return data


def data_trans(data, columns_names, code, istable=True):
    if columns_names:
        data = DataFrame([x for x in data], columns=columns_names)
    else:
        data = DataFrame([x for x in data])
    if code:
        exec code
        result = trans(data).fillna('')
    else:
        result = data.fillna('')
    if istable:
        result = to_table(result)
    return result


def trans(data, column_heads, rows_heads):
    code = r'''
def trans(data):
    result = data.groupby(['{}'])
    return result.sum().unstack()
    '''.format("','".join(column_heads))
    return data_trans(data, column_heads + rows_heads, code, True)


def get_table(data, rows_increment):
    if data:
        for item in data:
            try:
                if "buckets" in data[item]:
                    tmp_data = []
                    for it in data[item]['buckets']:
                        val = it['key']
                        tmp_table = get_table(it, rows_increment)
                        for i in tmp_table:
                            i.insert(0, val)
                        tmp_data.extend(tmp_table)
                    return tmp_data
            except:
                continue
        result = []
        for item in rows_increment:
            if "value" in data[item]:
                result.append(data[item]['value'])
        return [result]
    return []


def jsonify(*args, **kwargs):
    """ 序列化JSON 同时支持对 web—py query后返回的封装对象"""

    def default(items):
        if isinstance(items, IterBetter):
            return [item for item in items]  # 取出webpy数据库生成的结果对象
        return str(items)

    return dumps(default=kwargs.pop("default", default), *args, **kwargs)
