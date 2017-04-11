# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db

''' get the custom menus '''
def get_menus():
    result = []
    sql = """
        select * from t_chart_menu where status=1;
    """
    try:
        result = _metric_meta_db.query(sql)
    except Exception, e:
        pass
    return result

''' get the custom modules '''
def get_modules(module_types="",types=None):
    result = []
    where = ''
    if module_types:
        where += " and module_types='{}' ".format(module_types)
    if types != None:
        where += " and types={} ".format(types)
    sql = """
        select * from t_chart_modules where status=1 {};
    """.format(where)
    try:
        result = _metric_meta_db.query(sql)
    except Exception, e:
        pass
    return result