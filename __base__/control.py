# coding:utf-8
from __base__ import System
from abc import ABCMeta


class ControlBase(object):
    """ 控制层基类 """
    __metaclass__ = ABCMeta


class Control(ControlBase, System):
    """ 控制类 """
