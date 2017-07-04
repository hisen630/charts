# coding:utf-8
from __future__ import unicode_literals
from __base__ import RTC, ChartsError
from copy import deepcopy
from time import time as now
from pandas import DataFrame
from json import loads, dumps
from common.logger import logger
from common.utils import _req_url, to_table

from abc import ABCMeta, abstractmethod, abstractproperty

start_time = 1464754939523


class ElasticSearchAggs(dict):
    __metaclass__ = ABCMeta
    key = abstractproperty()  # 前置Key

    def __init__(self, column):
        super(ElasticSearchAggs, self).__init__()
        self.column = column
        self.body = self.setdefault(self.key, {"field": column["field"]})
        self.parse()  # 调用解析规则

    @abstractmethod
    def parse(self):
        """ 解析规则 """


class ElasticSearchLimit(dict):
    def __init__(self, limit=0):
        super(ElasticSearchLimit, self).__init__()
        self["size"] = limit


class ElasticSearchFiltered(dict):
    """ es 过滤对象"""
    __metaclass__ = ABCMeta
    key = abstractproperty()  # 前置Key

    def __init__(self, column):
        super(ElasticSearchFiltered, self).__init__()
        self.column = column
        self.body = self.setdefault(self.key, {}).setdefault(self.column["field"], {})
        self.parse()  # 调用解析规则

    @abstractmethod
    def parse(self):
        """ 解析规则 """


class DateRange(ElasticSearchFiltered):
    """  所有数据的基本的时间区间  """
    key = "range"
    start = property(lambda self: self.column.get("min") or 1464754939523)
    end = property(lambda self: self.column.get("max") or (now() * 1000))

    def parse(self):
        self.body.update({
            "gte": int(self.start),
            "lte": int(self.end),
            "format": "epoch_millis"
        })


class String(ElasticSearchAggs):
    key = "terms"

    def parse(self):
        order = self.column.get("order", "desc")
        assert order in ("desc", "asc")
        self.body.update({
            "size": int(self.column.get("size", 5)),
            "order": {self.column.get("order key", 1): order},

        })


class Date(ElasticSearchAggs):
    key = "date_histogram"
    interval = 1
    min_doc_count = 1
    time_zone = "Asia/Shanghai"
    min = property(lambda self: self.column.get("min") or 1464754939523)
    max = property(lambda self: self.column.get("max") or (now() * 1000))
    __interval_dome = "5m"  # 5分钟
    units = "daily"
    units_mappings = {
        "second": "s",
        "minute": "m",
        "hourly": "h",
        "daily": "d",
        "weekly": "w",
        "monthly": "M",
        "yearly": "y",
        None: "d"  # 默认天
    }
    get_interval = classmethod(lambda cls, interval, units:
                               "{}{}".format(interval, cls.units_mappings.get(units)))

    def parse(self):
        self.body.update({
            "time_zone": self.time_zone,
            "interval": self.get_interval(
                self.column.get("interval", self.interval), self.column.get("units", self.units)),
            "min_doc_count": self.min_doc_count,
            "extended_bounds": {"min": int(self.min), "max": int(self.max)},
        })


# class Ranges(ElasticSearchAggs):
#     key = "range"
#
#     def parse(self):
#         if "ranges" in self.column:
#             self.body.update({
#                 "ranges": [{"from": int(start), "to": int(end)} for start, end in self.column["ranges"]],
#                 "keyed": True
#             })
#         else:
#             self.clear()

class Number(dict):
    key = "range"

    def __init__(self, ):
        super(Number, self).__init__()
        self[self.key] = {}

    def parse(self):
        self.body.update({
            "ranges": [{"from": int(start), "to": int(end)} for start, end in self.column["ranges"]],
            "keyed": True
        })


types_mappings = {
    "string": String,
    "date": Date,
    # "number": Number,
}


class ElasticSearchRTC(RTC):
    """ ES request body 映射  每个实例解决一次解析 """
    type = 4

    default_request_body = {
        # "size": 0,
        "query": {
            "filtered": {
                "query": {
                    "query_string": {
                        # "query": "*",
                        "analyze_wildcard": True
                    }
                },
                "filter": {
                    "bool": {
                        "must": [
                            # {
                            #     "range": {
                            #         "task_date": {
                            #             "gte": 1464754939523,
                            #             "lte": 1496290939523,
                            #             "format": "epoch_millis"
                            #         }
                            #     }
                            # }
                        ],
                        "must_not": [],
                    }
                }
            }
        },
        "aggs": {
            #     "1": {
            #         "date_histogram": {
            #             "field": "task_date",
            #             "interval": "1M", # 按月聚合
            #             "time_zone": "Asia/Shanghai",
            #             "min_doc_count": 1,
            #             "extended_bounds": {
            #                 "min": 1464754939521,
            #                 "max": 1496290939521
            #             }
            #         },
            #         "aggs": {
            #             "2": {
            #                 "sum": {
            #                     "field": "gmv"
            #                 }
            #             },
            #             "3": {
            #                 "sum": {
            #                     "field": "month_sale"
            #                 }
            #             }
            #         }
            #     }
        }
    }
    _types_json = {"date_histogram": {"field": "task_date",
                                      "interval": "1M",
                                      "time_zone": "Asia/Shanghai",
                                      "min_doc_count": 1,
                                      "extended_bounds": {"min": 1464834955997, "max": 1496370955997}},
                   "terms": {
                       "field": "fg_category2_name.raw",
                       "size": 5,
                       "order": {"1": "desc"}
                   }}

    ai = 0  # es 请求体中使用到的数字Key

    def __init__(self, *args, **kwargs):
        """
        维度包含了指标 数据条数和排序规则
        """
        super(ElasticSearchRTC, self).__init__(*args, **kwargs)
        if not (self.columns and self.rows):
            raise ChartsError("请检查rows或columns是否为空")
        self.columns_copy = deepcopy(self.columns)
        self.request_body = deepcopy(self.default_request_body)  # 深拷贝 消除引用
        self.aggs_value = {}
        self.filed_rela = {}
        self.rows_increment = []
        self.request_body.update(ElasticSearchLimit(self.limit))
        self.request_body['query']['filtered']['query']['query_string']['query'] = self.query  # 设置Query
        for filter in self.filters:
            self.request_body["query"]['filtered']["filter"]["bool"]["must"].append(DateRange(filter))
        # self.request_body["query"]['filtered']["filter"]["bool"]["must_not"].append(DataRange(self.must_not))
        for self.ai, row in enumerate(self.rows, 1):
            key = str(self.ai)
            kv = self.rows_increment.append(key) or self.aggs_value.setdefault(key, {})
            kv['sum'] = kv_sum = {}
            self.filed_rela[key] = kv_sum.setdefault("field", row["field"])

        self.request_body['aggs'] = self.get_aggs()  # 设置查询参数

    def get_data(self):
        self.response = loads(_req_url(self.address, self.request_body))
        logger._print(dumps(self.response))

        if not self.response or 'aggregations' not in self.response:
            raise ChartsError("请求失败")
        data = self.get_table(self.response['aggregations'])
        if len(self.columns_copy) > 1:
            data = self.trans(data)
        else:
            heads = [item["field"] for item in self.columns_copy] + [item["field"] for item in self.rows]
            data.insert(0, heads)
        return data

    def trans(self, data):
        heads = []
        for column in self.columns_copy:
            heads.append(column["field"])
        for row in self.rows:
            heads.append(row["field"])
        code = r'''
def trans(data):
    result = data.groupby(['{}'])
    return result.sum().unstack()
        '''.format("','".join([item["field"] for item in self.columns_copy]))
        data = self.data_trans(data, heads, code, True)
        return data

    def data_trans(self, data, columns_fields, code, istable=True):
        if columns_fields:
            data = DataFrame([x for x in data], columns=columns_fields)
        else:
            data = DataFrame([x for x in data])
        if 1 == 1:
            if code:
                exec code
                result = trans(data).fillna('')
            else:
                result = data.fillna('')
            if istable:
                result = to_table(result)
            return result

    def get_table(self, data):
        if not data:
            return []
        for item in data:
            try:
                if "buckets" in data[item]:
                    tmp_data = []
                    for it in data[item]['buckets']:
                        val = it['key']
                        tmp_table = self.get_table(it)
                        for i in tmp_table:
                            i.insert(0, val)
                        tmp_data.extend(tmp_table)
                    return tmp_data
            except Exception, e:
                continue
        result = [data[item]['value'] for item in self.rows_increment if "value" in data[item]]
        return [result]

    def get_aggs(self):
        ai = self.ai = self.ai + 1  # 这里防止实例属性的引用
        column = self.columns.pop(0)
        type = column["type"]
        if type not in types_mappings:
            return {}  # # "该类型({})不支持，请联系管理员。".format(type)
        tmp = types_mappings.get(type)(column)

        self.filed_rela[self.ai] = column["field"]

        if self.columns:
            tmp['aggs'] = self.get_aggs()
            if not tmp['aggs']:
                return {}
            tmp['aggs'] = dict(tmp['aggs'], **self.aggs_value)
        else:
            tmp['aggs'] = self.aggs_value
        return {ai: tmp}


class Manager():
    types = 4

    def preview(self, **kwargs):
        return ElasticSearchRTC(**kwargs).get_data()
