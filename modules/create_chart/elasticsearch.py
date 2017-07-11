# coding:utf-8
from __future__ import unicode_literals
from abc import ABCMeta, abstractproperty
from __base__.api.es import (
    Search, Term, Match, Terms, Range,
    Avg, Sum, Max, Min, ExtendedStats, Cardinality,
    Histogram, DateHistogram
)

from __base__ import (
    RTC,
    APIError,
    ElasticSearchParamsParse,

)

from time import time as now
from json import loads, dumps
from common.base import get_table, trans
from common.utils import _req_url
from common.logger import logger


class CheckParams(object):
    """ 方法参数的映射与生成 """
    __metaclass__ = ABCMeta
    type = abstractproperty()


range_mappings = {
    ">=": "gte",
    ">": "gt",
    "<=": "lte",
    "<": "lt",
    "==": "ae",
}


class FilterCheckParams(CheckParams):
    type = "filters"

    @staticmethod
    def number(values):
        oper = {range_mappings[values["oper"]]: int(values["value"])}
        return mappings["number"]["filter"](values["field"], date=False, **oper)

    @staticmethod
    def string(values):
        return mappings["string"]["filter"][values["oper"]](values["field"], values["value"])

    @staticmethod
    def date(values):
        default_min = now() - 86400 * 60  # 俩月前
        oper = {"gte": int(values.get("min", default_min * 1000)), "lte": int(values.get("max", now() * 1000))}
        return mappings["date"]["filter"](values["field"], date=True, **oper)


class RowCheckParams(CheckParams):
    type = "rows"

    @staticmethod
    def number(values):
        return (mappings["number"]["aggregation"].get(values["agg"]) or Sum)(values["field"])


class ColumnCheckParams(CheckParams):
    type = "columns"
    orders = {
        "desc": True,
        "asc": False
    }

    @classmethod
    def string(cls, values):
        return mappings["string"]["aggregation"](
            values["field"], size=values["size"], reverse=cls.orders.get(values["order"]))

    @staticmethod
    def number(values):
        return mappings["number"]["aggregation"][values["oper"]](values["field"], values["interval"])

    @staticmethod
    def date(values):
        return mappings["date"]["aggregation"](values["field"], values["interval"].strip() + values["unit"])


checkers = (FilterCheckParams, RowCheckParams, ColumnCheckParams)

mappings = {
    "string": {
        "filter": {"包含": Term, "分词": Match},
        "aggregation": Terms
    },
    "date": {
        "filter": Range,
        "aggregation": DateHistogram
    },
    "number": {
        "filter": Range,
        "aggregation": {
            # 指标聚合
            "最大": Max, "最小": Min, "平均": Avg, "求和": Sum,
            "唯一值数量": Cardinality, "extended_stats": ExtendedStats,
            # 范围聚合
            "histogram": Histogram
        }},
}


class ElasticSearchRTC(RTC, ElasticSearchParamsParse):
    """ ES request body 映射  每个实例解决一次解析 """
    type = 4
    request_body = None

    get_heads = staticmethod(lambda items: [item["field"] for item in items])

    def __init__(self, *args, **kwargs):
        """
        维度包含了指标 数据条数和排序规则
        """
        super(ElasticSearchRTC, self).__init__(*args, **kwargs)
        if not (self.columns and self.rows):
            raise APIError("请检查rows或columns是否为空")
        self.request_body = Search().query(self.query)
        self.ai = 1
        self.rows_keys = []
        for index, (checker_type, checker) in enumerate(
                dict((checker.type, checker) for checker in checkers).items()):
            items = getattr(self, checker_type)
            for item in items:
                parse_function = getattr(checker, item["type"])
                assert parse_function, "{field}[{type}]不支持的类型".format(**item)
                if checker_type == FilterCheckParams.type:  # 过滤类型的api不同
                    self.request_body.filter_bool(must=parse_function(item))
                else:
                    self.request_body.aggs(self.ai, parse_function(item))
                    if checker_type == RowCheckParams.type:
                        self.rows_keys.append(str(self.ai))
                        self.ai += 1
        self.column_heads = self.get_heads(self.columns)
        self.row_heads = self.get_heads(self.rows)
        self.heads = self.column_heads + self.row_heads

    def get_data(self):
        logger.pprint(self.request_body)
        self.response = loads(_req_url(self.address, self.request_body))
        logger.pprint(self.response)
        if not self.response or 'aggregations' not in self.response:
            raise APIError("请求失败")
        data = get_table(self.response.get('aggregations', {}), self.rows_keys)
        if len(self.columns) > 1:
            data = trans(data, self.column_heads, self.row_heads)
        else:
            data.insert(0, self.heads)
        return data

        #     @classmethod
        #     def get_table(cls, data, rows_increment):
        #         if not data:
        #             return []
        #         for item in data:
        #             try:
        #                 if "buckets" in data[item]:
        #                     tmp_data = []
        #                     for it in data[item]['buckets']:
        #                         val = it['key']
        #                         tmp_table = cls.get_table(it, rows_increment)
        #                         for i in tmp_table:
        #                             i.insert(0, val)
        #                         tmp_data.extend(tmp_table)
        #                     return tmp_data
        #             except Exception, e:
        #                 continue
        #         result = []
        #         for item in rows_increment:
        #             if "value" in data[item]:
        #                 result.append(data[item]['value'])
        #         return [result]
        #
        #     def trans(self, data):
        #
        #         code = r'''
        # def trans(data):
        #     result = data.groupby(['{}'])
        #     return result.sum().unstack()
        #         '''.format("','".join([item["field"] for item in self.columns]))
        #         return self.data_trans(data, self.column_heads, code, True)
        #
        #     @staticmethod
        #     def data_trans(data, columns_names, code, istable=True):
        #         if columns_names:
        #             data = DataFrame([x for x in data], columns=columns_names)
        #         else:
        #             data = DataFrame([x for x in data])
        #         if code:
        #             exec code
        #             result = trans(data).fillna('')
        #         else:
        #             result = data.fillna('')
        #         if istable:
        #             result = to_table(result)
        #         return result

        # def format_result(self):
        #     aggregations = (self.response.get('aggregations', {}).values() or [{}])[0].get("buckets", [])
        #     result = []
        #
        #     for aggregation in aggregations:
        #         keys, value, buckets = [aggregation["key"]], 0, []
        #         for bucket in aggregation.itervalues():
        #             if isinstance(bucket, DictType):
        #                 if "value" in bucket:
        #                     value = bucket["value"]
        #                 if "buckets" in bucket:
        #                     buckets = bucket.get("buckets", [])
        #
        #         while buckets:
        #             for bucket in buckets:
        #                 values = []
        #                 keys.append(bucket["key"])
        #                 buckets = filter(self.filter_bucket, bucket.itervalues())
        #                 if not bucket:
        #                     keys
        #                 # for item in bucket.itervalues():
        #                 #     if isinstance(item, DictType):
        #                 #         if "value" in item:
        #                 #             value = item["value"]
        #                 #         else:
        #                 #             buckets = item.get("buckets", [])
        #                 print bucket
        #             break
        #         result.append(keys + [value])
        #         # item = filter(lambda item: isinstance(item, DictType) and "buckets" in item, bucket.values())
        #         # if not item:
        #         #     pass
        #         # row[bucket["key"]] = filter(ite)
        #         # bucket["key"]
        #         # if not item:
        #
        #         # print "[TEST]: ",
        #         # keys = []
        #         # while buckets:
        #         #     for bucket in buckets:
        #         #         key = key.setdefault(bucket["key"], {})
        #         #         for k, sub_bucket in bucket.iteritems():
        #         #             if isinstance(sub_bucket, DictType):
        #         #                 if "value" in sub_bucket:
        #         #                     key["value"] = sub_bucket["value"]
        #         #                 buckets = sub_bucket.get("buckets", [])
        #
        #         # for buckets in aggregations:  # 第一层循环 为了基本的维度
        #         #     row = {}
        #         #     keys = row.setdefault("keys", [])
        #         #     keys.append(buckets["key"])
        #         #     while buckets:
        #         #
        #         #         for key, bucket in buckets.iteritems():
        #         #             if isinstance(bucket, DictType):
        #         #                 if "value" in bucket:
        #         #                     row["value"] = bucket["value"]
        #
        #         # for keys, sub_buckets in bucket.iteritems() if isinstance(bucket, DictType) else []:
        #         #     if isinstance(sub_buckets, DictType):
        #         #         if "value" in sub_buckets:
        #         #             result.append([keys, bucket.get("key")])
        #         #
        #     print "\n\n\n\n\n"
        #     # print keys
        #     # print values
        #     logger.pprint(result)

        # result_item = []
        #

        #
        # buckets = 1


# heads = []
#         for column in self.columns:
#             heads.append(column["field"])
#         for row in self.rows:
#             heads.append(row["field"])
#         code = r'''
# def trans(data):
#     result = data.groupby(['{}'])
#     return result.sum().unstack()
#         '''.format("','".join([item["field"] for item in self.columns]))
#         data = self.data_trans(data, heads, code, True)
#         return data


class Manager():
    types = 4

    def preview(self, **kwargs):
        return ElasticSearchRTC(**kwargs).get_data()
