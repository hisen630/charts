# coding:utf-8
from conf.__base__ import ConfigBase
from abc import abstractproperty


class ConfigDefault(ConfigBase):
    # TIME_COLUMN = abstractproperty()
    _time_column = abstractproperty()
    modules_name = abstractproperty()  # 映射 modules 文件夹地址
    _notebook_path = abstractproperty()  # notebook 保存路径
    _notebook_url = abstractproperty()  # notebook URl地址
    _customs_name = abstractproperty()  # 全局设置名称,用于控制自定义全局参数的key，默认为any
    hive_is_have_dbs = abstractproperty()  # hive查询表时是否包含表名
    _is_auth = abstractproperty()  # 是否开启用户验证
    _auth_white_list = abstractproperty()
    ELASTIC_SEARCH_API_URL = abstractproperty()  # ES API地址
    MYSQL_CONFIG_FILE = abstractproperty()  # 数据库配置文件
    LOG_LEVEL = abstractproperty()  # 日志级别
