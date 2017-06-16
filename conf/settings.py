# -*- coding: utf-8 -*-

from __base__ import ConfigBase
from logging import INFO


class Config(ConfigBase):
    _time_column = "tasks_date_time"
    modules_name = 'modules'
    # notebook save path
    # _notebook_path = "c:/Users/jianczhang/"
    _notebook_path = "/home/jianczhang/notebook"
    # notebook url
    # _notebook_url = "http://localhost:8888"
    _notebook_url = "http://notebook.in.hillinsight.com"
    # 全局设置名称,用于控制自定义全局参数的key，默认为any
    _customs_name = "any"
    # hive查询表时是否包含表名
    hive_is_have_dbs = False
    # __hive_is_have_dbs = True

    # auth all ;if you want to stop the auth,please set _is_auth=False
    _is_auth = False
    _auth_white_list = ["/dashboard/get_chart", "/chart/get_chart", "/"]
    ELASTIC_SEARCH_API_URL = "http://hi-prod-19:9200/{}/{}/_search"
    MYSQL_CONFIG_FILE = "/home/work/conf/storage/mysql.conf"
    LOG_LEVEL = INFO
