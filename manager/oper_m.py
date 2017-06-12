# -*- coding: utf-8 -*-
from base.oper_b import get_data_by_ids


def get_data(ids=(), name=None):
    result = get_data_by_ids(ids)
    final_result = {}
    for item in result:
        final_result.setdefault(item["ds_types"], {}).setdefault(item["fields_types"], {}).setdefault(
            "opers", {}).setdefault(item["oper"], item["id"])
    return final_result
