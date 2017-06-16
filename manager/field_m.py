# -*- coding: utf-8 -*-
from base.field_b import FieldBase
from json import loads


class FieldManager:
    @staticmethod
    def get_data(ids=()):
        field_result = []
        for item in FieldBase.get_data_by_ids(ids):
            if item.get("status", 0) == 0:
                continue
            item["columns"] = loads(item.get("columns", "[]").strip())

            field_result.append(item)
        return field_result
        # 这里要分析dbs 字段的类型  是Z那种数据源

    @staticmethod
    def get_by_id(id):
        return (FieldBase.get_data_by_ids(id) or [{}, ])[0]
