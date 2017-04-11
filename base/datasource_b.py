# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db

'''get datasource from table by id'''
def get_data_by_id(sid):
    result = []
    sql = """
        select * from t_chart_datasource where id={} and status=1;
    """.format(int(sid))
    try:
        result = _metric_meta_db.query(sql)
        if result:
            result = result[0]
    except Exception, e:
        pass
    return result

'''get datasource from table by ids'''
def get_data_by_ids(sids):
    result = []
    sids = [str(x) for x in sids]
    sql = """
        select * from t_chart_datasource where id in ({});
    """.format(",".join(sids))
    try:
        result = _metric_meta_db.query(sql)
    except Exception, e:
        pass
    return result

'''get datasource from table by name'''
def get_data_by_name(name,status=[1],other=0):
    result = []
    where = ''
    if status:
        where += ' and status in ({}) '.format(status)
    if other:
        where += ' and id not in ({}) '.format(other)
    sql = """
        select * from t_chart_datasource where name="{}" {};
    """.format(name,where)
    try:
        result = _metric_meta_db.query(sql)
        if result:
            result = result[0]
    except Exception, e:
        pass
    return result

'''save datasource to table'''
def save(form):
    hid = _metric_meta_db.insert('t_chart_datasource',**form)
    return hid

'''update datasource by id'''
def update(form):
    _metric_meta_db.update('t_chart_datasource',where="id={}".format(form['id']),**form)
    return form['id']

'''get datasource list'''
def get_datasource_list(sid="",name="",iscount=False,current=1,rowCount=20):
    where = []
    limit = ''
    if sid:
        if type(sid) == int:
            sid = [sid]
        where.append("""and id in ({})""".format(",".join(map(str,sid))))
    if name:
        where.append("""and name like "%{}%" """.format(name))
    if rowCount:
        stc = (int(current)-1)*int(rowCount)
        if not stc:
            stc = 0
        limit = "limit {},{}".format(int(current)-1,rowCount)
    content = "*"
    orders = "order by id desc"
    if iscount:
        limit = ""
        orders = ""
        content = "count(*) as c"
    sql = """
        select {} from t_chart_datasource where status=1 {} {} {};
    """.format(content," ".join(where),orders,limit)
    result = _metric_meta_db.query(sql)
    if iscount:
        if result:
            return result[0]['c']
        else:
            return 0
    else:
        if result:
            return result
        else:
            return []
