# -*- coding: utf-8 -*-
from __base__ import ChartsError, AssertionError, Mapping
from re import compile
from requests import get
from flask import request
from route import CustomView
from common.base import jsonify
from manager.source_m import SourceManager


class Source(CustomView):
    es_index_regex = compile(r"(?:green|yellow)\s+open\s(.*?)\s")

    # 列表页
    def index(self):
        return jsonify(Mapping.TYPES_MAPPING)
        # 获取数据

    def list(self):
        return jsonify(SourceManager.list(int(request.args["id"])))

    def edit(self):
        json = {
            "id": 1,
            "index_to_dimension": [{"field": "task_date"}],
            "dimension_to_index": [{"field": "bg_category3_id"}],
            "address_label": "测试1",
        }
        json = request.get_json(force=True)
        assert json.get("id"), "请回传ID."
        assert SourceManager.edit(json), "数据已更新或更新失败."
        return jsonify({"status":True, "msg":"ok"})

    # 保存方法
    def save(self):
        pass

    def search(self):
        """ 不搜索就是常用 """
        args = dict(request.args.to_dict(), **request.form.to_dict())
        return jsonify(SourceManager.get_data(args.pop("id", ())))
