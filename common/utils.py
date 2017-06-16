#coding=utf-8
import os
import re
import urllib2
import urllib
from decimal import Decimal
import json
import glob
import time

from pandas import DataFrame,Series
import pandas as pd;import numpy as np
from collections import Iterable as IterType
from logging import getLogger, DEBUG

logger = getLogger()
logger.setLevel(DEBUG)

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False

def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

def dictToSql(data,inner=None,outer=None):
    result = {}
    if data:
        if type(inner) == list:
            for key in inner:
                if key in data:
                    result[key] = r"`{}`='{}'".format(key,data[key])
        else:
            for key in data:
                result[key] = r"`{}`='{}'".format(key,data[key])
        if type(outer) == list:
            for key in outer:
                if key in data:
                    del data[key]
    return result.values()
def defaultencode(obj):
    if isinstance(obj, Decimal):
        # Subclass float with custom repr?
        return fakefloat(obj)

    import calendar, datetime,time

    if isinstance(obj, datetime.datetime):
        return "{}".format(obj)
    if isinstance(obj, datetime.date):
        return "{}".format(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")
class fakefloat(float):
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return str(self._value)

def get_trans_punc_func():
    """中文标点转换为英文标点"""
    punc_mapping = {
        u'“':u'"',
        u'”':u'"',
        u'·':u'.',
        u'。':u'.',
        u'！':u'!',
        u'……':u'......',
        u'（':u'(',
        u'）':u')',
        u'——':u'--',
        u'【':u'[',
        u'】':u']',
        u'{':u'{',
        u'}':u'}',
        u'‘':u'\'',
        u'’':u'\'',
        u'，':u',',
        u'？':u'?',
        u'：':u':',
        u'；':u';',
        u'《':u'<',
        u'》':u'>'
                   }

    def _transform_punctuation(ustring):
        char_list = []
        for c in ustring:
            if c in punc_mapping:
                char_list.append(punc_mapping[c])
            else:
                char_list.append(c)
        return ''.join(char_list)
    return _transform_punctuation

transform_punctuation = get_trans_punc_func()

def _get_dedup_empty():
    """将连续空白符替换成单个空白符"""
    import re
    multi_empty_p = re.compile(r'\s{2,}')

    def _dedup_empty(ustr):
        return multi_empty_p.subn(u' ', ustr)[0]
    return _dedup_empty

dedup_empty = _get_dedup_empty()

def _get_remove_bracket():
    """去掉括号内的信息"""
    import re
    bracket_p = re.compile(r'(\(.*\))')

    def _remove_bracket(ustr):
        return bracket_p.subn(u'', ustr)[0]
    return _remove_bracket

remove_bracket = _get_remove_bracket()


def split_by_cn_en(ustring):
    """将ustring按照中文，字母分开"""
    retList=[]
    utmp=[]
    _state = 0 # 0非中文，1非英文
    _split = False # 当前状态是否产生一个分割
    for uchar in ustring:
        if is_chinese(uchar):
            if _state == 0:
                _split = True
            _state = 1

        elif is_alphabet(uchar):
            if _state == 1:
                _split = True
            _state = 0

        if _split:
            if len(utmp) > 0:
                retList.append(''.join(utmp))
                utmp = []
            _split = False

        utmp.append(uchar)

    if len(utmp) > 0:
        retList.append(''.join(utmp))

    return retList


from datetime import datetime, timedelta

def get_lastmonth_str(date_str):
    month_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    last_month = month_obj - timedelta(days=1)
    return '%d-%02d-01'%(last_month.year, last_month.month)

def get_lastyearmonth_str(date_str):
    month_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    last_year = month_obj - timedelta(days=365)
    return '%d-%02d-01'%(last_year.year, last_year.month)

def normalize_str4brand(u_str, encoding='utf-8'):
    if not isinstance(u_str, unicode) and isinstance(u_str, str):
        u_str = u_str.decode(encoding)
    assert isinstance(u_str, unicode)

    u_str = u_str.lower()
    u_str = strQ2B(u_str)
    u_str = transform_punctuation(u_str)
    u_str = dedup_empty(u_str)
    u_str = u_str.strip()
    u_str = remove_bracket(u_str)

    return u_str


def cluster_brands(brands_list, one_one_mapping=None, kw_mapping=None, kw_match=1.0, split_symbol='/', cn_split=False):
    '''
    brands_list - 待进行聚类的品牌列表。顺序很重要，同一类别内的品牌，排在第一个的将作为主品牌
    one_one_mapping - 一对一映射，仅接受dict类型参数。内容为 alias -> principle brand。
    kw_mapping - 品牌的关键词映射，格式为 主品牌 -> set(关键词1， 关键词2 ...)
    kw_match - 在进行关键词匹配时，若该值为整型则至少要匹配上这么多个关键词，并以匹配上最多的作为主品牌；若为浮点型，则至少要匹配上该浮点数表示的百分比的关键词。
    split_symbol - 对于brands_list中的品牌，使用该符号进行切分以得到品牌关键词
    cn_split - 是否进行中英文切分，若设置成True，则会在中英文分界处进行切分
    '''

    if one_one_mapping is None:
        one_one_mapping = {}
    if kw_mapping is None:
        kw_mapping = {}

    _tmp_one_one_mapping = {}
    for alias, principle in one_one_mapping.items():
        _tmp_one_one_mapping[normalize_str4brand(alias)] = principle

    _tmp_kw_mapping = {}
    for principle, kw_set in kw_mapping.items():
        for kw in kw_set:
            _tmp_kw_mapping[normalize_str4brand(kw)] = principle


    brands_cluster = {} # brand -> set of brands

    for brand in brands_list:
        normalized_brand = normalize_str4brand(brand)

        # direct one one mapping
        one_one_brand = _tmp_one_one_mapping.get(normalized_brand, None)
        if one_one_brand:
            if one_one_brand not in brands_cluster:
                brands_cluster[one_one_brand] = set()
            brands_cluster[one_one_brand].add(brand) # 最终输出的聚类内部都是归一化前的
            continue
        one_one_brand = _tmp_one_one_mapping.get(brand, None)
        if one_one_brand:
            if one_one_brand not in brands_cluster:
                brands_cluster[one_one_brand] = set()
            brands_cluster[one_one_brand].add(brand) # 最终输出的聚类内部都是归一化前的
            continue


        # try kw match
        if split_symbol:
            symbol_kw_set = set(normalized_brand.split(split_symbol))
        else:
            symbol_kw_set = set([normalized_brand,])

        if cn_split:
            kw_set = set()
            for kw in symbol_kw_set:
                kw_set.update(split_by_cn_en(kw))
        else:
            kw_set = symbol_kw_set

        candidate_dict = {} # principle -> count
        for kw in kw_set:
            principle = _tmp_kw_mapping.get(kw,None)
            if principle:
                if principle not in candidate_dict:
                    candidate_dict[principle] = 0
                candidate_dict[principle] += 1
        if candidate_dict:
            candidate_tuple_list = sorted(candidate_dict.items(), key=lambda k:k[1], reverse=True)
            found = False
            if isinstance(kw_match, float):
                percent = candidate_tuple_list[0][1]*1.0/len(kw_set)
                if percent >= kw_match:
                    found = True
            elif isinstance(kw_match, int):
                if candidate_tuple_list[0][1] >= kw_match:
                    found = True
            else:
                raise TypeError("Need float or int")
            if found:
                if candidate_tuple_list[0][0] not in brands_cluster:
                    brands_cluster[candidate_tuple_list[0][0]] = set()
                brands_cluster[candidate_tuple_list[0][0]].add(brand)
                # 将当前品牌的关键词加到主品牌的关键词列表中，以扩大召回
                for kw in kw_set:
                    if kw not in _tmp_kw_mapping:
                        _tmp_kw_mapping[kw] = candidate_tuple_list[0][0]
                continue

        # cluster
        brands_cluster[brand] = set([brand,])
        for kw in kw_set:
            if kw not in _tmp_kw_mapping:
                _tmp_kw_mapping[kw] = brand

    return brands_cluster
def array_column(data,format,format_str=False):
    """取list或者dict 二级下面的某列，比如 直接从数据库返回的结果我想取name列，[{'name'：'fds','id':1},{'name':'fdsa','id':2}]"""
    result = []
    if type(format) == str:
        if format.strip() == '':
            pass
        else:
            if type(data) == list:
                for i in data:
                    if format_str and ( type(i[format]) == datetime.date or type(i[format]) == datetime.datetime):
                        result.append(i[format].isoformat())
                    else:
                        result.append(i[format])
            elif type(data) == dict:
                for idx,i in enumerate(data):
                    if format_str and ( type(i[format]) == datetime.date or type(i[format]) == datetime.datetime):
                        result.append(i[format].isoformat())
                    else:
                        result.append(i[format])
    return result
def dbFormatToDict(data,format):
    """从list或者dict里面以某列数据作为dict 的index 比如从数据库返回的结果我将name列作为index变为dict，[{'name'：'fds','id':1},{'name':'fdsa','id':2}]"""
    result = {}
    if type(format) == str:
        if format.strip() == '':
            result = data
        else:
            for i in data:
                result[i[format]] = i
    elif (type(format) == list and format) or (type(format) == dict and format):
        for i in data:
            index = ''
            for j in format:
                index += i[j]
            result[index] = i
    return result
def _format_hql(content):
    return content.replace('`','')

def heqExec(hql):
    if os.system('''hive -e "{}" >/dev/null 2>&1'''.format(_format_hql(hql))):
        return False
    else:
        return True

def is_exist_hive(table):
    if os.system(''' hive -e "show create table {};" '''.format(_format_hql(table))):
        return False
    else:
        return True

def sumStr(string):
    from hashlib import md5
    m = md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

def get_hive_column(h_table):
    p = os.popen(''' hive -e "desc {};" '''.format(h_table))
    table_info = p.read().decode('utf-8')
    result = []
    part = []
    table_info = table_info.split('\n')
    for item in table_info:
        m = item.split('\t')
        m = m[0].strip()
        if "#" in m or not m:
            pass
        elif m not in result:
            result.append(m)
        elif m in result:
            part.append(m)
    if p.close():
        result = []
        part = []

    return [result,part]

def get_hive_location(h_table):
    p = os.popen(''' hive -e "desc formatted {};" '''.format(h_table))
    table_info = p.readlines()
    location = ''
    if table_info:
        for item in table_info:
            item = item.decode('utf-8')
            if 'Location:' in item and 'hdfs:' in item and 'db' in item:
                table = item.split("\t",1)
                location = table[1].strip()
    if p.close():
        location = ''
    return location
def get_partitions(h_table):
    p = os.popen(''' hive -e "show partitions {};"|tail -n1 '''.format(h_table))
    table_info = p.readlines()
    result = ''
    if table_info:
        for item in table_info:
            item = item.decode('utf-8')
            result = item
    if p.close():
        result = ''
    return result
def get_uniquekey(db,table):
    result = ''
    _match = re.compile(r"(`.*`)")
    try:
        p = db.query('show create table {};'.format(table))
        for it in p:
            it = it['Create Table']
            it = it.split('\n')
            for item in it:
                if 'PRIMARY KEY'.lower() in item.lower():
                    result = _match.search(item).group(0).replace("`","")
                if 'UNIQUE key'.lower() in item.lower() or 'UNIQUE index'.lower() in item.lower():
                    result = _match.search(item).group(0).replace("`","")
    except Exception, e:
        pass
    return result
    pass
def handle_hive_sort(create_sql):
    return create_sql
    sql = ''
    if create_sql:
        create_sql = create_sql.lower()
        create_sql = re.sub(";(\s)*$","",create_sql).strip()
        if 'stored as' in create_sql:
            sql = create_sql
        else:
            _p = re.compile('\(.*\).*(location.*)')
            m = _p.search(create_sql)
            if m:
                s = m.groups()
                if s:
                    _m = s[-1]
                    sql = create_sql.replace(r'{}'.format(_m),' STORED AS RCFILE {}'.format(_m))
            else:
                sql = "{} STORED AS RCFILE".format(create_sql)
    return sql+";"

def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[e]
    return _json_obj

def format_ifram_url(url,search):
    return url.replace(r"query:'*'",r"query:'{}'").format(search).replace(r'height="600" width="800"',r'height="352" width="100%"')

def _req_url(url,data):
    repeat = 4
    req = ''
    data = json.dumps(data)
    for j in range(repeat):
        # try:
        logger.debug("Request {}.".format(url))
        res = urllib2.Request(url,data)
        req = urllib2.urlopen(res).read()
        break
        # except Exception, e:
        #     pass
    if req == '':
        raise Exception(url+u"获取不到数据")
    return req

def _req_url_body(url,data,isput=False):
    repeat = 4
    req = ''
    data = json.dumps(data)
    for j in range(repeat):
        # try:
        res = urllib2.Request(url,data, {'Content-Type': 'application/json'})
        if isput:
            res.get_method = lambda: 'PUT'
        req = urllib2.urlopen(res).read()
        break
        # except Exception, e:
        #     pass
    if req == '':
        raise Exception(url+u"获取不到数据")
    return req

def get_py_file(dirs):
    result = []
    if dirs:
        for item in glob.glob(dirs):
            module_name,ext = os.path.splitext(os.path.basename(item))
            if ext == ".py" and module_name != "__init__":
                result.append(module_name)
    return result

def format_number(data):
    result = []
    for item in data:
        tmp = {}
        for it in item:
            tmp[it] = item[it]
            if type(tmp[it]) == str or type(tmp[it]) == unicode:
                try:
                    if r"." in item[it]:
                        if r',' in item[it]:
                            t = item[it].replace(",","")
                            tmp[it] = float(t)
                        else:
                            tmp[it] = float(item[it])
                    elif r',' in item[it]:
                        t = item[it].replace(",","")
                        tmp[it] = int(t)
                    else:
                        tmp[it] = int(item[it])
                except Exception, e:
                    pass
        if tmp:
            result.append(tmp)
    return result


def data_trans(data,columns_names,code,istable=True):
    if columns_names:
        data = DataFrame([x for x in format_number(data)],columns=columns_names)
    else:
        data = DataFrame([x for x in format_number(data)])
    try:
        if code:
            exec code
            result = trans(data).fillna('')
        else:
            result = data.fillna('')
        if istable:
            result = to_table(result)
        return result
    except Exception, e:
        return False

def muti_data_trans(data,code,istable=True):
    try:
        if not code:
            code = "def trans(frame):\n    return frame[0]"
        exec code
        result = trans(data).fillna('')
        if istable:
            result = to_table(result)
        return result
    except Exception, e:
        return False

def to_table(frame):
    columns = frame.columns
    indexs = frame.index
    if indexs.name:
        header = [indexs.name]+columns.values.tolist()
    else:
        header = columns.values.tolist()
    indexs_list = frame.index.values.tolist()
    data = np.array(frame).tolist()
    if indexs.name:
        tmp = [item.insert(0,indexs_list[key]) for key,item in enumerate(data)]
    data.insert(0,header)
    return data

def to_dict(table,insert_header=[],isHeader=True):
    header = table[0]
    data = []
    for key,item in enumerate(table):
        if key != 0:
            tmp = {}
            for t_i in insert_header:
                for t in t_i:
                    tmp[t] = t_i[t]
            for k,it in enumerate(item):
                tmp[header[k]] = it
            data.append(tmp)
    if isHeader:
        if insert_header:
            for t_i in insert_header:
                for t in t_i:
                    header.insert(0,t)
        return header,data
    else:
        return data

def get_time(isnow=True):
    if isnow:
        times = time.strftime("%Y-%m-%d %X",time.localtime(time.time()))
    else:
        times = "2038-01-01 00:00:00"
    return times


# ============================================================================
def to_iter(items=()):
    """ 转换为迭代类型
        1 -> [1, ]
        (1, 2) -> (1, 2)
        "123" -> ["123", ]
    """
    return items if isinstance(items, IterType) and not isinstance(items, basestring) else [items]