# -*- coding: utf-8 -*-

#Create a unified handle to prevent the creation of multiple links to the database
from hillinsight.storage.db_conn import _mysql_config
_metric_meta_db = _mysql_config['god_metric_meta']['master']['offline']