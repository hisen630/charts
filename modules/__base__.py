# coding:utf-8
from abc import ABCMeta, abstractproperty


class MappingBase(object):
    """ 映射层 基类 """
    __metaclass__ = ABCMeta
    type = abstractproperty()  # 类型


class DataSourceMappingBase(MappingBase):
    """ 数据源映射 """


class TaskMappingBase(MappingBase):
    """ 任务类型映射 """
