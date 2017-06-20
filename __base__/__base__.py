# coding:utf-8
"""
    该工程下所有类均从这里继承
"""
from abc import ABCMeta


class SystemBase(object):
    """ 整个系统(工程)的基类 """
    __metaclass__ = ABCMeta


class System(SystemBase):
    """ 系统类 """


del ABCMeta  # 从当前引用空间内删除
