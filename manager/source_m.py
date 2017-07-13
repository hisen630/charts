# -*- coding: utf-8 -*-
from re import search
from json import loads
from base.source_b import SourceBase


def r1(pattern, string):
    result = search(pattern, string)
    if result:
        return result.group(1)


class SourceManager:
    @staticmethod
    def parse_address(address_string):
        agreement, args = address_string.split("://", 1)
        if "mysql" in agreement:
            args += "/"
        address, index, type, id = args.split("/")  # 索引 类型 id（mysql hive不支持）
        if "@" in address:
            address = r1(r"@(.*)", address)
        return agreement, address, index, type, id

    @classmethod
    def get_data(cls, ids=()):
        field_result = {}
        for item in SourceBase.get_data_by_ids(ids):
            if item.get("status", 0) == 0:
                continue
            _, address, index, type, _ = cls.parse_address(item.pop("address"))
            address = item.get("address_label", address)
            for column in loads(item.get("columns") or "[]"):
                unit = "index" if column["type"] == "number" else "dimension"
                field_result.setdefault("@".join([address, index]), {}).setdefault(type, {}).setdefault(
                    unit, []).append(dict(column, **{"id": item["id"], "source_type": item["type"]}))
        return field_result

    @staticmethod
    def get_by_id(id):
        return (SourceBase.get_data_by_ids(id) or [{}, ])[0]
