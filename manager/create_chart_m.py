# coding:utf-8
"""  创建图表 """
from __base__ import APIError
from json import loads
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

    filter_one = staticmethod(lambda name, fields: (filter(lambda item: item.get("field") == name, fields) or ({},))[0])

    @classmethod
    def preview(cls, **kwargs):
        """ 预览界面 
            参数检查和字段核对在这里完成
        """
        source_info = SourceManager.get_by_id(kwargs.pop("field_id"))
        if not source_info:
            raise APIError("数据不存在.")
        fields = loads(source_info.get("columns", "{}"))
        for items in (kwargs["columns"], kwargs["rows"]):
            for item in items:
                # 操作符过滤
                hit = cls.filter_one(item["name"], fields)
                if hit:
                    item["type"] = hit["type"]
                raise APIError("该行列({})不存在预置数据中.".format(item["name"]))

        return cls.get_model(source_info.pop("type", kwargs.pop("type"))).preview(  # 默认es
            **dict(kwargs, **{"address": source_info["address"]}))
