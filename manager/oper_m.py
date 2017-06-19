# -*- coding: utf-8 -*-
from base.oper_b import OperBase
from conf.default import TYPES_MAPPING


class OperManager:
    types_mappings = dict((y, x) for x, y in TYPES_MAPPING.items())

    @classmethod
    def get_data(cls, ids=()):
        result = OperBase.get_data_by_ids(ids)
        final_result = {}
        for item in result:
            final_result.setdefault(cls.types_mappings[item["ds_types"]], {}).setdefault(
                item["fields_types"], {}).setdefault(item["oper"], item["id"])
        return final_result

    @staticmethod
    def get_by_id(id):
        return (OperBase.get_data_by_ids(id) or [{}, ])[0]
