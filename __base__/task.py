# coding:utf-8
from abc import abstractmethod
from mapping import TaskMappingBase


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



