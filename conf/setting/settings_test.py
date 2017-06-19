# -*- coding: utf-8 -*-
from __base__ import ConfigDefault
from logging import DEBUG


class Config(ConfigDefault):
    _time_column = "tasks_date_time"
    MODULES_NAME = 'modules'
    NOTEBOOK_PATH = "c:/Users/jianczhang/"
    NOTEBOOK_URL = "http://localhost:8888"
    _customs_name = "any"
    HIVE_IS_HAVE_DBS = True
    IF_AUTH = False
    AUTH_WHITE_LIST = ["/dashboard/get_chart", "/chart/get_chart", "/"]
    MYSQL_CONFIG_FILE = "/Users/luoruiqing/work/charts/hillinsight/storage/mysql.conf"
    LOG_LEVEL = DEBUG
    ELASTIC_SEARCH_API_URL = "http://127.0.0.1:9999/{}/{}/_search"


if __name__ == '__main__':
    Config()
