# -*- coding: utf-8 -*-

from __base__ import ConfigDefault
from logging import INFO


class Config(ConfigDefault):
    _time_column = "tasks_date_time"
    MODULES_NAME = 'modules'
    _notebook_path = "/home/jianczhang/notebook"
    _notebook_url = "http://notebook.in.hillinsight.com"
    _customs_name = "any"
    hive_is_have_dbs = False
    IF_AUTH = False
    AUTH_WHITE_LIST = ["/dashboard/get_chart", "/chart/get_chart", "/"]
    ELASTIC_SEARCH_API_URL = "http://hi-prod-19:9200/{}/{}/_search"
    MYSQL_CONFIG_FILE = "/home/work/conf/storage/mysql.conf"
    LOG_LEVEL = INFO
