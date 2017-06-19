# coding:utf-8
from abc import ABCMeta


class ToolsBase(object):
    """ 工具基类 """
    __metaclass__ = ABCMeta

    def __str__(self):
        return "TOOL: " + super(ToolsBase, self).__str__()
