# coding:utf-8
from abc import ABCMeta


class DataBase(object):
    """ 数据层基础类 """
    __metaclass__ = ABCMeta


class Data(DataBase):
    """ 数据类 """
