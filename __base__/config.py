# coding:utf-8
from __base__ import System
from abc import ABCMeta, abstractproperty


class ConfigBase(object):
    """ 配置基类 """
    __metaclass__ = ABCMeta


class Config(ConfigBase, System):
    """ 配置类 """


class ConfigDefault(Config):
    """ 默认配置类 """
    # TIME_COLUMN = abstractproperty()
    _time_column = abstractproperty()
    _customs_name = abstractproperty()  # 全局设置名称,用于控制自定义全局参数的key，默认为any

    MODULES_NAME = abstractproperty()  # 映射 modules 文件夹地址
    NOTEBOOK_PATH = abstractproperty()  # notebook 保存路径
    NOTEBOOK_URL = abstractproperty()  # notebook URl地址
    HIVE_IS_HAVE_DBS = abstractproperty()  # hive查询表时是否包含表名
    IF_AUTH = abstractproperty()  # 是否开启用户验证
    AUTH_WHITE_LIST = abstractproperty()  # 无需认证的URL
    ELASTIC_SEARCH_API_URL = abstractproperty()  # ES API地址
    MYSQL_CONFIG_FILE = abstractproperty()  # 数据库配置文件
    LOG_LEVEL = abstractproperty()  # 日志级别
