# coding:utf-8
"""  创建图表 """
from __base__ import APIError, NotImplementedManagerMappingTypeError, AssertionError
from json import loads
from source_m import SourceManager
from common.base import get_module_object
from modules.create_chart import mappings
from manager.oper_m import OperManager


class CreateChartManager:
    """ 创建表管理者 """
    _modules_split = 'create_chart'

    @classmethod
    def preview(cls, **kwargs):
        """ 预览界面 
            参数检查和字段核对在这里完成
        """
        source_info = SourceManager.get_by_id(kwargs.pop("source_id"))
        if not source_info:
            raise APIError("该数据不存在.")
        all_field = kwargs["columns"] + kwargs["rows"]
        req_fields = dict((item["field"], item) for item in all_field)
        for field in loads(source_info.get("columns", "[]")):
            req_fields.get(field["field"], {})["type"] = field["type"]
        for item in all_field:
            assert "type" in item, "该字段({})不存在预置数据中.".format(item["field"])

        module = mappings[source_info.pop("type", kwargs.pop("type", 4))](
            **dict(kwargs, **{"address": source_info["address"]}))
        return module.get_data()

    @classmethod
    def save(cls, **kwargs):
        raise NotImplementedManagerMappingTypeError()