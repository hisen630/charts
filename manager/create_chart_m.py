# coding:utf-8
"""  创建图表 """
from json import loads
from modules.create_chart.mysql import Manager
from field_m import FieldManager
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

    def get_sql(self):
        pass

    @classmethod
    def preview(cls, field_id, column_name, oper_id, types=3):
        """ 预览界面 """
        row = FieldManager.get_by_id(field_id)

        if not row:
            return {"status": 0, "msg": "数据不存在"}
        row["columns"] = columns = (filter(lambda item: item.get("field") == column_name,
                                           loads(row.get("columns", "{}"))) or ({},))[0]
        if not columns:
            return {"status": 0, "msg": "数据库存在，但该数据列不存在，请在常用设置内添加字段"}
        oper = OperManager.get_by_id(oper_id)
        if not oper:
            return {"status": 0, "msg": "该操作符记录不存在"}
        model = cls.get_model(types)
        model.preview(row, oper)
        return row

    @staticmethod
    def save(field_id, column_name, oper_id):
        row = FieldManager.get_by_id(field_id)

        if not row:
            return {"status": 0, "msg": "数据不存在"}
        row["columns"] = columns = (filter(lambda item: item.get("field") == column_name,
                                           loads(row.get("columns", "{}"))) or ({},))[0]
        if not columns:
            return {"status": 0, "msg": "数据库存在，但该数据列不存在，请在常用设置内添加字段"}
        oper = OperManager.get_by_id(oper_id)
        if not oper:
            return {"status": 0, "msg": "该操作符记录不存在"}

        return row
