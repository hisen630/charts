# coding:utf-8
from __base__ import System
from abc import ABCMeta, abstractmethod, abstractproperty
from mapping import Mapping1


class TaskBase(object):
    """ 任务基类 """
    __metaclass__ = ABCMeta


class Task(TaskBase, System):
    """ 任务层 """


class TaskMappingBase(Task, Mapping1):
    """ 任务类型映射 """
    types = abstractproperty()  # 类型 兼容老版本代码


class TaskMapping(TaskMappingBase):
    """ 映射不同数据任务抽象类 """
    types = 0  # 默认为mysql类型

    @abstractmethod
    def save_dict(self, form):
        """ 保存方法 - 转换为可保存的字典类型 """

    @abstractmethod
    def get_datasource(self, data):
        """ 获得数据 提出配置，转换为字典，以便渲染 """

    @abstractmethod
    def get_data(self):
        """ 获得数据 """

    def get_data_group(self):
        """ 获得数据分组 """
        raise NotImplementedError()

    def run_task(self):
        """ 运行任务 """
        raise NotImplementedError()
