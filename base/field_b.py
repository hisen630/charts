# -*- coding: utf-8 -*-
from common.db_sum import _metric_meta_db
from common.sql_tools import Where


class FieldBase:
    @staticmethod
    def get_data_by_ids(ids=()):
        """ 暂时只支持根据ID搜索 或者多选 """
        where = Where("id").in_(ids)
        if where:
            where = "WHERE {};".format(where)

        return _metric_meta_db.query("SELECT * FROM `t_chart_fields` {};".format(where)) or []
