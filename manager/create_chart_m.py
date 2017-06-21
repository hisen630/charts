# coding:utf-8
"""  创建图表 """
from __base__ import APIError
from json import loads
from modules.create_chart.mysql import Manager
from source_m import SourceManager
from common.base import get_module_object
from manager.oper_m import OperManager


class CreateChartManager:
    """ 创建表管理者 """
    _modules_split = 'create_chart'

    @classmethod
    def get_model(cls, types):
        objects = get_module_object(cls._modules_split)
        for item in objects:
            if objects[item].types == types:
                return objects[item]
        raise NotImplemented("未实现的映射方法")

    @classmethod
    def preview(cls, **kwargs):
        """ 预览界面 """
        source_info = SourceManager.get_by_id(kwargs["field_id"])
        if not source_info:
            raise APIError("数据不存在.")
        fields = loads(source_info.get("columns", "{}"))
        for column in kwargs["columns"]:
            if not (filter(lambda item: item.get("field") == column["name"], fields) or ({},))[0]:
                raise APIError("该列({})不存在预置数据中.".format(column["name"]))
        for row in kwargs["rows"]:
            if not (filter(lambda item: item.get("field") == row["name"], fields) or ({},))[0]:
                raise APIError("该行({})不存在预置数据中.".format(row["name"]))
                # 操作符过滤
        print source_info["address"]
        return {}
        # return cls.get_model(kwargs.pop("type", 4)).preview(**kwargs)
