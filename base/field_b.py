# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db


def where_in(items=()):
    """ 接受一个可迭代对象 有元素或无元素  
        1. 有元素且超出1个  IN （x,y,.......）
        2. 只有一个元素     = x
        3. 无元素          "" # 空字符
    """
    if not items:
        return ""
    if len(items) == 1:
        return "{}".format(items)
    return "IN ({})".format(",".join(map(str, items)))


def get_data_by_ids(ids=()):
    """ 暂时只支持根据ID搜索 或者多选 """
    return _metric_meta_db.query("SELECT * FROM `t_chart_fields` WHERE id {};".format(where_in(ids)))
