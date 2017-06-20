# coding:utf-8
from __base__ import System
from abc import ABCMeta


class DataBase(object):
    """ 数据层基础类 """
    __metaclass__ = ABCMeta


class Data(DataBase, System):
    """ 数据类 """
