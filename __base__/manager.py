# coding:utf-8
from __base__ import System
from common.base import get_module_object
from error import NotImplementedManagerMappingTypeError
from abc import ABCMeta, abstractproperty


class ManagerBase(object):
    """ 管理基类 """
    __metaclass__ = ABCMeta


class Manager(ManagerBase, System):
    """ 管理类 """
    MODULE_PATH = abstractproperty()  # 指定文件夹地址

    @classmethod
    def get_model(cls, type):
        objects = get_module_object(cls.MODULE_PATH)
        for item in objects:
            if getattr(objects[item], "type") == type:
                return objects[item]
        raise NotImplementedManagerMappingTypeError()
