# coding:utf-8

from __base__ import RTCB
from json import loads
from common.utils import _req_url
from pandas import DataFrame
from common.utils import to_table


class ElasticSearchRTC(RTCB):
    """ ES request body 映射  每个实例解决一次解析 """
    type = 4

    default_request_body = {
        "size": 0,
        "query": {
            "filtered": {
                "query": {
                    "query_string": {
                        "query": "*",
                        "analyze_wildcard": True
                    }
                },
                "filter": {
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "task_date": {
                                        "gte": 1464754939523,
                                        "lte": 1496290939523,
                                        "format": "epoch_millis"
                                    }
                                }
                            }
                        ],
                        "must_not": []
                    }
                }
            }
        },
        "aggs": {
            "1": {
                "date_histogram": {
                    "field": "task_date",
                    "interval": "1M",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1,
                    "extended_bounds": {
                        "min": 1464754939521,
                        "max": 1496290939521
                    }
                },
                "aggs": {
                    "2": {
                        "sum": {
                            "field": "gmv"
                        }
                    },
                    "3": {
                        "sum": {
                            "field": "month_sale"
                        }
                    }
                }
            }
        }
    }
    _types_json = {"date_histogram": {"field": "task_date",
                                      "interval": "1M",
                                      "time_zone": "Asia/Shanghai",
                                      "min_doc_count": 1,
                                      "extended_bounds": {"min": 1464834955997, "max": 1496370955997}},
                   "terms": {"field": "fg_category2_name.raw", "size": 5, "order": {"1": "desc"}}}

    from conf.default import ELASTIC_SEARCH_API_URL as api

    def __init__(self, *args, **kwargs):
        super(ElasticSearchRTC, self).__init__(*args, **kwargs)
        if not self.columns and self.rows:
            raise Exception("请检查rows或columns是否为空")
        self.request_body = self.default_request_body.copy()
        self.request_body['query']['filtered']['query']['query_string']['query'] = self.query
        self.url = self.api.format(self.index_or_db, self.type_or_table)

        self.ai = 0

        self.aggs_value = {}
        self.filed_rela = {}
        self.rows_increment = []
        for self.ai, item in enumerate(self.rows, 1):
            field, value = item.split("__")
            if value != "value": break
            key = str(self.ai)
            kv = self.rows_increment.append(key) or self.aggs_value.setdefault(key, {})
            self.filed_rela[key] = field
            kv['sum'] = {"field": "{}".format(field)}

        self.request_body['aggs'] = self.get_aggs()

    def get_data(self):
        self.response = loads(_req_url(self.url, self.request_body))
        if not self.response or 'aggregations' not in self.response:
            raise Exception("请求失败")
        data = self.get_table(self.response['aggregations'])

        if len(self.columns) > 1:
            data = self.trans(data)
        else:
            heads = [item.split("__")[0] for item in self.columns] + [item.split("__")[0] for item in self.rows]
            data.insert(0, heads)
        return data

    def trans(self, data):
        heads = []
        for item in self.columns:
            heads.append(item.split("__")[0])
        for item in self.rows:
            heads.append(item.split("__")[0])
        code = r'''
def trans(data):
    result = data.groupby(['{}'])
    return result.sum().unstack()
        '''.format("','".join([item.split("__")[0] for item in self.columns]))
        data = self.data_trans(data, heads, code, True)
        return data

    def data_trans(self, data, columns_names, code, istable=True):
        if columns_names:
            data = DataFrame([x for x in data], columns=columns_names)
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
        self.ai += 1
        field_name, type = self.columns.pop(0).split("__")

        if type not in self._types_json:
            return {}

        tmp = {type: self._types_json[type], "aggs": {}}
        tmp[type]['field'] = field_name
        self.filed_rela[self.ai] = field_name

        if len(self.columns) > 0:
            tmp['aggs'] = aggs = self.get_aggs()
            if not aggs:
                return {}
        else:
            tmp['aggs'] = self.aggs_value
        return {self.ai: tmp}


class Manager():
    types = 3

    def preview(self, row, oper):
        ElasticSearch().get_data()
