# coding:utf-8
from __base__ import System
from abc import ABCMeta, abstractproperty


class MappingBase(object):
    """ 映射层 基类 """
    __metaclass__ = ABCMeta


class Mapping(MappingBase, System):
    """ 数据源映射 """
    type = abstractproperty()  # 类型


class Mapping1(MappingBase, System):  # Mapping1 为了兼容老代码
    types = abstractproperty()  # 类型
