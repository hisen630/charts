# -*- coding: utf-8 -*-
from flask import request
from route import CustomView
from common.base import jsonify
from manager.oper_m import OperManager


class Oper(CustomView):
    # 列表页
    def index(self):
        pass

    # 编辑
    def edit(self):
        pass

    # 保存方法
    def save(self):
        pass

    # 获取数据
    def get_data(self):
        pass

    # 获取sql
    def get_sql(self):
        pass

    def search(self):
        """ 不搜索就是常用 """
        args = dict(request.args.to_dict(), **request.form.to_dict())
        return jsonify(OperManager.get_data(args.pop("id", ())))
