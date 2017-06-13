# -*- coding: utf-8 -*-
from base.field_b import get_data_by_ids
from json import loads


def get_data(ids=(), name=None):
    field_result = []
    for item in get_data_by_ids(ids):
        if item.get("status", 0) == 0:
            continue
        item["columns"] = loads(item.get("columns","{}"))
        field_result.append(item)
    return field_result
    # 这里要分析dbs 字段的类型  是Z那种数据源
