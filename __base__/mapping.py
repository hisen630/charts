# coding:utf-8
from __base__ import System
from abc import ABCMeta, abstractproperty


class MappingBase(object):
    """ 映射层 基类 """
    __metaclass__ = ABCMeta
    TYPES_MAPPING = abstractproperty()  # 映射关系


class Mapping(MappingBase):
    """ 映射层实现类 """
    type = abstractproperty()  # 类型
    TYPES_MAPPING = {
        0: 'MysqlDB',
        1: 'MysqlCaculate',  # mysql任务型
        2: 'FakeCube',
        3: 'Hive',
        4: 'ElasticSearch'
    }


class Mapping1(Mapping, System):  # Mapping1 为了兼容老代码
    types = abstractproperty()  # 类型
