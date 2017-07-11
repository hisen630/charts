# coding:utf-8
from __base__ import System
from abc import ABCMeta, abstractproperty


class ElasticSearchBase(object):
    """ 映射层 基类 """
    __metaclass__ = ABCMeta


class ElasticSearch(ElasticSearchBase, System):
    """ 映射层实现类 """


class ElasticSearchParseBase(ElasticSearch):
    """ 解析基础 """


class ElasticSearchParse(ElasticSearchParseBase):
    """ 解析实现 """


class ElasticSearchParamsParse(dict, ElasticSearchParse):
    """ body 对象 """

    # query_mapping = abstractproperty()
    # filtered_mapping = abstractproperty()
    # aggregation_mapping = abstractproperty()


class ElasticSearchQuery(dict, ElasticSearchParse):
    """ Query对象 """


class ElasticSearchFiltered(dict, ElasticSearchParse):
    """ Filter 对象 """
    key = abstractproperty()


class ElasticSearchAggregation(dict, ElasticSearchParse):
    """ 聚合对象 """
    key = abstractproperty()


if __name__ == '__main__':
    class Test(ElasticSearchParamsParse):
        query_mapping, filtered_mapping, aggregation_mapping = [None] * 3

    print Test()
