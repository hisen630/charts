# coding:utf-8
from __future__ import unicode_literals
from __base__ import ChartsError
from json import dumps
from route import CustomView
from common.logger import logger
from flask import request, jsonify
from common.base import render_custom
from manager.oper_m import OperManager
from manager.source_m import SourceManager
from manager.create_chart_m import CreateChartManager


class CreateChart(CustomView):
    def __init__(self):
        self.manager = CreateChartManager()

    def index(self):
        dbs = SourceManager.get_data()
        mappings = OperManager.get_data()
        return render_custom("/createchart/createchart.tpl", dbs=dbs, mappings=mappings)

    def preview(self):  # TODO 必须post提交方式
        # http://127.0.0.1:16688/createchart/preview?field_id=1&cid=1&rid=1
        # if request.method != "POST":
        #     return Response("请用POST方式提交.", status=400)

        json = {
            "source_id": 1,
            "rows": [
                {"field": "gmv", "oid": 1},
                # {"field": "month_sale", "oid": 1}
            ],
            "columns": [
                {"field": "fg_category2_name.raw", "size": 5, "order": "desc"},
                # {"field": "fg_category4_name.raw", "size": 5, "order": "desc"},
                # {"field": "category2_id", "ranges": [(50510002, 50510003), (60510003, 60510004)]},
                # {"field": "data_test", "type": "date", "interval": 15, "units": "hourly"},

            ],
            "filters": [
                {"field": "task_date"}
            ],
            "query": 'fg_category2_name.raw:"零食/坚果/特产"',
            "limit": 0  # 0代表所有
        }
        json = request.get_json(force=True)
        json["type"] = 4  # 强制类型为es类型

        logger.pprint("request json:" + dumps(json))
        try:
            result = {'status': True, "code": 0, 'msg': u'获取数据完成.', "data": self.manager.preview(**json)}
        except ChartsError, e:
            result = {"status": e.status, "code": e.code, "msg": e.message, "data": None}
        return jsonify(result)

    def save(self):
        return dumps(self.manager.save())
