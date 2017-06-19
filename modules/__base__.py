# coding:utf-8
from abc import ABCMeta, abstractproperty


class MappingBase(object):
    """ 映射层 基类 """
    __metaclass__ = ABCMeta


class DataSourceMappingBase(MappingBase):
    """ 数据源映射 """
    type = abstractproperty()  # 类型


class TaskMappingBase(MappingBase):
    """ 任务类型映射 """
    types = abstractproperty()  # 类型 兼容老版本代码


class NotebookBase(object):
    """ NoteBook 基类 """
    __metaclass__ = ABCMeta
