# -*- coding: utf-8 -*-
debug = True  # TODO 这里要注意更改状态 每次上线保证状态为Flase
_time_column = "tasks_date_time"
_modules_name = 'modules'
# notebook save path
# _notebook_path = "c:/Users/jianczhang/"
_notebook_path = "/home/jianczhang/notebook"
# notebook url
# _notebook_url = "http://localhost:8888"
_notebook_url = "http://notebook.in.hillinsight.com"
# 全局设置名称,用于控制自定义全局参数的key，默认为any
_customs_name = "any"
# hive查询表时是否包含表名
__hive_is_have_dbs = False
# __hive_is_have_dbs = True

# auth all ;if you want to stop the auth,please set _is_auth=False
_is_auth = False
_auth_white_list = ["/dashboard/get_chart", "/chart/get_chart", "/"]
if debug:  # 调试状态
    api = "http://127.0.0.1:9999/{}/{}/_search"
else:  # 线上状态
    api = "http://hi-prod-19:9200/{}/{}/_search"
