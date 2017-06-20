# coding:utf-8
from __base__ import System
from abc import ABCMeta


class ManagerBase(object):
    """ 管理基类 """
    __metaclass__ = ABCMeta


class Manager(ManagerBase, System):
    """ 管理类 """
