# -*- coding: utf-8 -*-
from base.field_b import FieldBase
from json import loads


class FieldManager:
    @staticmethod
    def get_data(ids=()):
        field_result = {}
        for item in FieldBase.get_data_by_ids(ids):
            if item.get("status", 0) == 0:
                continue
            dbs = item.pop("dbs", "").strip().rsplit("/", 1)[1]
            item["columns"] = loads(item["columns"])
            field_result.setdefault(dbs, {}).setdefault(item.pop("tables"), item)
        return field_result

    @staticmethod
    def get_by_id(id):
        return (FieldBase.get_data_by_ids(id) or [{}, ])[0]
