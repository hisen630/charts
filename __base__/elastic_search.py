# coding:utf-8
from __base__ import System
from abc import ABCMeta, abstractproperty


class ElasticSearchBase(object):
    """ 映射层 基类 """
    __metaclass__ = ABCMeta


class ElasticSearch(ElasticSearchBase, System):
    """ 映射层实现类 """


class ElasticSearchRequest(ElasticSearch):
    """ 请求对象 """


class ElasticSearchQuery(ElasticSearchRequest):
    """ Query对象 """


class ElasticSearchFiltered(ElasticSearchRequest):
    """ Filter 对象 """


class ElasticSearchAggs(ElasticSearchRequest):
    """ Aggs对象 """
