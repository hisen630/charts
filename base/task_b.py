# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db

'''get task by id'''
def get_data_by_id(sid):
    result = []
    sql = """
        select * from t_chart_task where id={} and status=1;
    """.format(int(sid))
    try:
        result = _metric_meta_db.query(sql)
        if result:
            result = result[0]
    except Exception, e:
        pass
    return result

'''get task by ids '''
def get_data_by_ids(sids):
    result = []
    sids = [str(x) for x in sids]
    sql = """
        select * from t_chart_task where id in ({});
    """.format(",".join(sids))
    try:
        result = _metric_meta_db.query(sql)
    except Exception, e:
        pass
    return result

'''get task by name'''
def get_data_by_name(name,status=[1],other=0):
    result = []
    where = ''
    if status:
        where += ' and status in ({}) '.format(status)
    if other:
        where += ' and id not in ({}) '.format(other)
    sql = """
        select * from t_chart_task where name="{}" {};
    """.format(name,where)
    try:
        result = _metric_meta_db.query(sql)
        if result:
            result = result[0]
    except Exception, e:
        pass
    return result

'''save data to task'''
def save(form):
    hid = _metric_meta_db.insert('t_chart_task',**form)
    return hid

'''update data to task'''
def update(form):
    _metric_meta_db.update('t_chart_task',where="id={}".format(form['id']),**form)
    return form['id']

'''get task list'''
def get_task_list(sid="",name="",iscount=False,current=1,rowCount=20,types=0):
    where = []
    limit = ''
    if sid:
        if type(sid) == int:
            sid = [sid]
        where.append("""and id in ({})""".format(",".join(map(str,sid))))
    if name:
        where.append("""and name like "%{}%" """.format(name))
    if types:
        where.append("""and types = {} """.format(int(types)))
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
        select {} from t_chart_task where status=1 {} {} {};
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

'''get relation tables'''
def get_relation_info(ids,table_tag=""):
    where = ""
    if table_tag:
        where = r""" and table_tag = "{}" """.format(table_tag)
    sql = "select * from t_chart_task_relation where tid={} {}".format(ids,where)
    result = _metric_meta_db.query(sql)
    if result:
        return result
    else:
        return []


'''get run log list'''
def get_runlog_list(sid="",name="",iscount=False,current=1,rowCount=20,types=0):
    where = []
    limit = ''
    if sid:
        if type(sid) == int:
            sid = [sid]
        where.append("""and b.id in ({})""".format(",".join(map(str,sid))))
    if name:
        where.append("""and b.name like "%{}%" """.format(name))
    if types:
        where.append("""and b.types = {} """.format(int(types)))
    if rowCount:
        stc = (int(current)-1)*int(rowCount)
        if not stc:
            stc = 0
        limit = "limit {},{}".format(stc,rowCount)
    content = "a.id,b.name,a.types,a.run_time,a.st,a.et,a.msg,a.status"
    orders = "order by a.id desc"
    if iscount:
        limit = ""
        content = "count(b.name) as c"
        orders = ""
    sql = """
        select {} from t_chart_task_log a left join t_chart_task b on a.tid=b.id where b.status=1 {} {} {} ;
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

'''get run log by id'''
def get_runlog_by_id(sid):
    result = []
    sql = """
        select * from t_chart_task_log where id={};
    """.format(int(sid))
    try:
        result = _metric_meta_db.query(sql)
        if result:
            result = result[0]
    except Exception, e:
        pass
    return result

'''init task log(insert task log) '''
def init_task_log(form):
    hid = _metric_meta_db.insert('t_chart_task_log',**form)
    return hid

'''update task log'''
def update_task_log(form):
    _metric_meta_db.update('t_chart_task_log',where="id={}".format(form['id']),**form)
    return form['id']

'''get task by id'''
def get_task(ids):
    sql = "select * from t_chart_task where status=1 and id={};".format(ids)
    result = _metric_meta_db.query(sql)
    if result:
        return result[0]
    return result
