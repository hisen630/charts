# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db
from common.utils import get_time

'''get task data from data by id and time'''
def get_task(sid,times=""):
    result = []
    if times == "":
        times = get_time()
    sql = """
        select * from t_chart_task where status=1 and st>="{}" and et<="{}";
    """.format(int(sid))
    try:
        result = _metric_meta_db.query(sql)
    except Exception, e:
        pass
    return result
