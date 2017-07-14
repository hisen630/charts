# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from re import search
from json import loads, dumps
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

    edit_pattern = {
        "index_to_dimension": ("index", "dimension"),
        "dimension_to_index": ("dimension", "index")
    }

    @classmethod
    def edit(cls, json):
        source = (SourceBase.get_data_by_ids(json["id"]) or [{}])[0]
        assert source, "不存在的ID"
        di_map = dict((k, loads(source.get(k, "[]"))) for k in ("index", "dimension"))
        di_map_keys = dict((dk, dict((item["field"], item) for item in dv)) for dk, dv in di_map.items())

        for key, (_from, _to) in cls.edit_pattern.items():
            for item in json.get(key, []):
                assert item["field"] in di_map_keys[_from], "提交的指标数据不再指标列中."
                if item["field"] not in di_map_keys[_to]:
                    hit = di_map_keys[_from].pop(item["field"])
                    di_map.setdefault(_to, []).append(hit)
                    di_map[_from].remove(hit)
        di_map = dict((k, dumps(v)) for k, v in di_map.items())
        di_map.update({
            "id": source["id"],
            "address_label": json.get("address_label", "").strip() or source["address_label"],
        })
        return SourceBase.update(**di_map)

    @staticmethod
    def list(id):
        source = (SourceBase.get_data_by_ids(id) or [{}])[0]
        source.setdefault("index", loads(source.pop("index", "[]")))
        source.setdefault("dimension", loads(source.pop("dimension", "[]")))
        return source

    @classmethod
    def get_data(cls, ids=()):
        field_result = {}
        for item in SourceBase.get_data_by_ids(ids):
            if item.get("status", 0) == 0:
                continue
            _, address, index, type, _ = cls.parse_address(item.pop("address"))
            field_result.setdefault("@".join([item.get("address_label", address), index]), {})[type] = {
                "id": item["id"],
                "index": loads(item["index"] or "[]"),
                "dimension": loads(item["dimension"] or "[]")
            }
        return field_result

    @staticmethod
    def get_by_id(id):
        return (SourceBase.get_data_by_ids(id) or [{}, ])[0]
