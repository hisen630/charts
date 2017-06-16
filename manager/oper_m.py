# -*- coding: utf-8 -*-
from base.oper_b import OperBase


class OperManager:
    @staticmethod
    def get_data(ids=()):
        result = OperBase.get_data_by_ids(ids)
        final_result = {}
        for item in result:
            final_result.setdefault(item["ds_types"], {}).setdefault(item["fields_types"], {}).setdefault(
                "opers", {}).setdefault(item["oper"], item["id"])
        return final_result

    @staticmethod
    def get_by_id(id):
        return (OperBase.get_data_by_ids(id) or [{}, ])[0]
