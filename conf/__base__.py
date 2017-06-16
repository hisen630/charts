# coding:utf-8

from abc import ABCMeta, abstractproperty


class ConfigBase(object):
    __metaclass__ = ABCMeta

    _time_column = abstractproperty()
    _modules_name = abstractproperty()
    _notebook_path = abstractproperty()
    _notebook_url = abstractproperty()
    _customs_name = abstractproperty()
    hive_is_have_dbs = abstractproperty()
    _is_auth = abstractproperty()  # 是否开启用户验证
    _auth_white_list = abstractproperty()
    elastic_search_api = abstractproperty()  # ES API地址
