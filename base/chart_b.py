# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db


'''get the data from table by name'''
def get_data_by_name(name,status=[1],other=0):
    result = []
    where = ''
    if status:
        status = ",".join([str(x) for x in status])
        where += ' and status in ({}) '.format(status)
    if other:
        where += ' and id not in ({}) '.format(other)
    sql = """
        select * from t_chart_reports where name="{}" {};
    """.format(name,where)
    try:
        result = _metric_meta_db.query(sql)
        if result:
            result = result[0]
    except Exception, e:
        pass
    return result
    
'''get the data from table by id'''
def get_data_by_id(sid):
    result = []
    sql = """
        select * from t_chart_reports where id={} and status=1;
    """.format(int(sid))
    try:
        result = _metric_meta_db.query(sql)
        if result:
            result = result[0]
    except Exception, e:
        pass
    return result

'''save data to chart table'''
def save(form):
    hid = _metric_meta_db.insert('t_chart_reports',**form)
    return hid

'''update chart table's data by id '''
def update(form):
    _metric_meta_db.update('t_chart_reports',where="id={}".format(form['id']),**form)
    return form['id']

'''get highchart_edit json'''
def get_chart(chart,data):
    result = {}
    if chart and data:
        if chart.get('series',False):
            first = data[0]
            data = get_column_combine(data)
            lens = len(data)
            series = chart['series']
            for key,item in enumerate(series):
                item['name'] = item['name'].encode('utf-8')
                if key<lens:
                    item['data'] = data[key]
                else:
                    item['data'] = []
            chart['series'] = series
            result = chart
    return result

'''parse new data to highchart_edit json data'''
def get_column_combine(data):
    result = []
    if data:
        lens = len(data[0])
        if lens > 0:
            result = [[] for i in xrange(lens)]
            for key,item in enumerate(data):
                if key>0:
                    for k,it in enumerate(item):
                        if k>0:
                            if it == '':
                                result[k-1].append([item[0],None])
                            else:
                                if type(it) == str or type(it) == unicode:
                                    try:
                                        if r"." in it:
                                            it = float(it)
                                        else:
                                            it = int(it)
                                    except Exception, e:
                                        pass
                                result[k-1].append([item[0],it])
    return result

'''get the chart list'''
def get_chart_list(sid="",name="",iscount=False,current=1,rowCount=20):
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
        content = "count(*) as c"
        orders = ""
    sql = """
        select {} from t_chart_reports where status=1 {} {} {};
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
