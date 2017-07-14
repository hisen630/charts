# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from common.db_sum import _metric_meta_db
from common.sql_tools import Where


class SourceBase:
    @staticmethod
    def get_data_by_ids(ids=()):
        """ 暂时只支持根据ID搜索 或者多选 """
        where = Where("id").in_(ids)
        if where:
            where = "WHERE {};".format(where)

        return _metric_meta_db.query("SELECT * FROM `t_chart_source` {};".format(where)) or []

    @staticmethod
    def update(id, index, dimension, address_label):
        return _metric_meta_db.query(
            "UPDATE `t_chart_source` SET `address_label` = $address_label, `index` = $index, `dimension` = $dimension WHERE `id` = $id ;",
            {
                "id": id,
                "address_label": address_label,
                "index": index,
                "dimension": dimension,
            })
