# -*- coding: utf-8 -*-
from re import search
from base.field_b import FieldBase
from json import loads


def r1(pattern, string):
    result = search(pattern, string)
    if result:
        return result.group(1)


class FieldManager:
    @staticmethod
    def get_data(ids=()):
        field_result = {}
        for item in FieldBase.get_data_by_ids(ids):
            if item.get("status", 0) == 0:
                continue
            address = item.pop("address")
            if item["type"] == 0:
                address += "/"
            address, index, type, id = address.split("://", 1)[1].split("/")  # 索引 类型 id（mysql hive不支持）
            if "@" in address:
                address = r1(r"@(.*)", address)
            for column in loads(item["columns"]):
                field_result.setdefault("@".join([address, index]), {}).setdefault(type, {}).setdefault(
                    column["class"], []).append(dict(column, **{"id": item["id"]}))
        return field_result

    @staticmethod
    def get_by_id(id):
        return (FieldBase.get_data_by_ids(id) or [{}, ])[0]
