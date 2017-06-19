# -*- coding: utf-8 -*-
from base.field_b import FieldBase
from json import loads


class FieldManager:
    @staticmethod
    def get_data(ids=()):
        field_result = {}
        for item in FieldBase.get_data_by_ids(ids):
            db = None
            if item.get("status", 0) == 0:
                continue
            dbs = item["dbs"].strip()
            if dbs.startswith("mysql"):
                dbs, db = dbs.rsplit("/", 1)
            if not db:
                continue
            field_result.setdefault(dbs, {}).setdefault(db, {}).setdefault(
                item["tables"], []).append(loads(item["columns"]))
        return field_result
        # 这里要分析dbs 字段的类型  是Z那种数据源

    @staticmethod
    def get_by_id(id):
        return (FieldBase.get_data_by_ids(id) or [{}, ])[0]
