# coding:utf-8
from abc import ABCMeta, abstractproperty


class MappingBase(object):
    """ 映射层 基类 """
    __metaclass__ = ABCMeta


class Mapping(MappingBase):
    """ 数据源映射 """
    type = abstractproperty()  # 类型


class Mapping1(MappingBase):
    types = abstractproperty()  # 类型
