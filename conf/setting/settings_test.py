# -*- coding: utf-8 -*-
from __base__ import ConfigDefault
from logging import DEBUG


class Config(ConfigDefault):
    _time_column = "tasks_date_time"
    MODULES_NAME = 'modules'
    _notebook_path = "c:/Users/jianczhang/"
    _notebook_url = "http://localhost:8888"
    _customs_name = "any"
    hive_is_have_dbs = True
    _is_auth = False
    _auth_white_list = ["/dashboard/get_chart", "/chart/get_chart", "/"]
    elastic_search_api = "http://127.0.0.1:9999/{}/{}/_search"
    MYSQL_CONFIG_FILE = "/Users/luoruiqing/work/charts/hillinsight/storage/mysql.conf"
    LOG_LEVEL = DEBUG
    ELASTIC_SEARCH_API_URL = "http://127.0.0.1:9999/{}/{}/_search"


if __name__ == '__main__':
    Config()
