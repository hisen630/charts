# coding:utf-8
from __base__ import System
from abc import ABCMeta, abstractmethod


class NotebookBase(object):
    """ NoteBook 基类 """
    __metaclass__ = ABCMeta


class Notebook(NotebookBase, System):
    """ TASK的 Notebook 抽象类 和 强制方法 """

    @abstractmethod
    def check_notebook_params(self):
        """ 检查创建notebook时参数是否正确 """

    @abstractmethod
    def create_notebook_code(self):
        """ 生成notebook代码 """
