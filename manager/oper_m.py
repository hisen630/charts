# -*- coding: utf-8 -*-
from base.oper_b import OperBase
from conf.default import TYPES_MAPPING
from modules import mappings


class OperManager:
    types_mappings = TYPES_MAPPING.copy()

    @classmethod
    def get_data(cls, ids=()):
        return mappings

    @staticmethod
    def get_by_id(id):
        return (OperBase.get_data_by_ids(id) or [{}, ])[0]
