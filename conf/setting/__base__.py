# coding:utf-8
from conf.__base__ import ConfigBase
from abc import abstractproperty


class ConfigDefault(ConfigBase):
    # TIME_COLUMN = abstractproperty()
    _time_column = abstractproperty()
    modules_name = abstractproperty()
    _notebook_path = abstractproperty()
    _notebook_url = abstractproperty()
    _customs_name = abstractproperty()
    hive_is_have_dbs = abstractproperty()
    _is_auth = abstractproperty()  # 是否开启用户验证
    _auth_white_list = abstractproperty()
    ELASTIC_SEARCH_API_URL = abstractproperty()  # ES API地址
    MYSQL_CONFIG_FILE = abstractproperty()  # 数据库配置文件
    LOG_LEVEL = abstractproperty()  # 日志级别