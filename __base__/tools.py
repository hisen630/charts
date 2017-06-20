# coding:utf-8
from __base__ import System
from abc import ABCMeta


class ToolsBase(object):
    """ 工具基类 """
    __metaclass__ = ABCMeta


class Tools(ToolsBase, System):
    """ 工具类 """
