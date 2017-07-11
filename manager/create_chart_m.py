# coding:utf-8
"""  创建图表 """
from abc import abstractproperty, ABCMeta
from __base__ import APIError, NotImplementedManagerMappingTypeError, AssertionError
from json import loads
from source_m import SourceManager
from modules.create_chart.elasticsearch import checkers
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
        all_field = kwargs["columns"] + kwargs["rows"] + kwargs["filters"]
        req_fields = dict((item["field"], item) for item in all_field)
        for field in loads(source_info.get("columns", "[]")):
            req_fields.get(field["field"], {})["type"] = field["type"]  # 添加类型

        for type in ("columns", "rows", "filters"):  # 三个区域提交的数据验证
            checker = (filter(lambda checker: checker.type == type, checkers) or [{}])[0]
            items = kwargs.get(type, [])
            assert checker, "不支持的提交类型"
            if type != "filters":
                assert items, "至少有一条可用数据"
            for item in items:
                assert "type" in item, "该字段({})不存在预置数据中.".format(item["field"])
                params = getattr(checker, item["type"], None)
                assert params, "{}功能下的{}类型没有被实现".format(type, item["type"])

        # # 所有filter类型的字段检查 =====================================================
        # for item in kwargs["filters"]:
        #     if item["type"] in ("number", "string"):  # TODO 数字过滤应该是范围形式，同时也应该支持单个字段的范围
        #         assert item.get("value"), APIError("{}字段没有填入内容".format(item["field"]))
        #         if item["type"] == "number":
        #             item["value"] = int(item["value"])
        #     if item["type"] in ("date"):
        #         assert item.get("min") or item.get("max"), APIError("{}字段需要开始时间或结束时间至少一项".format(item["field"]))
        # # rows 类型的字段检查 =========================================================
        # rows = kwargs.get("row", [])
        # assert rows, APIError("rows 内至少提交一列")
        # for row in rows:
        #     row["type"]
        # columns = kwargs.get("columns", [])
        # assert columns, APIError("columns 内至少提交一列")
        # for column in columns:
        #     pass
        # # 所有filter类型的字段检查 =====================================================
        assert "type" in kwargs, " 不支持的数据库类型"
        assert source_info["type"] == kwargs.pop("type", None), "绑定的数据类型发生了变化"
        module = mappings[source_info["type"]](  # 找到数据类型
            **dict(kwargs, **{"address": source_info["address"]}))
        return module.get_data()

    @classmethod
    def save(cls, **kwargs):
        raise NotImplementedManagerMappingTypeError()

    _ = {
        "filters": {"number": None},
        "rows": [],
        "columns": []
    }
