# coding:utf-8
from __base__ import System
from abc import ABCMeta


class LogicBase(object):
    """ 逻辑层基类 """
    __metaclass__ = ABCMeta


class Logic(LogicBase, System):
    """ 逻辑类 """
