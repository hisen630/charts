# -*- coding: utf-8 -*-

# Create a unified handle to prevent the creation of multiple links to the database
from hillinsight.storage.db_conn import _mysql_config
from conf.default import debug

_metric_meta_db = _mysql_config['god_metric_meta']['master']['offline']

if debug:  # debug状态下打印sql
    query = _metric_meta_db.query


    def print_sql(sql, *args, **kwargs):
        """ 负责SQL打印 在debug状态下"""
        print "[SQL]: ", sql
        return query(sql, *args, **kwargs)


    _metric_meta_db.query = print_sql
