# coding:utf-8
from json import dumps
from flask import request
from route import CustomView
from manager.create_chart_m import CreateChartManager


class CreateChart(CustomView):
    def __init__(self):
        self.manager = CreateChartManager()

    def preview(self):
        # http://127.0.0.1:16688/createchart/preview?field_id=1&cid=1&rid=1
        # if request.method != "POST":
        #     return Response("请用POST方式提交.", status=400)
        _ = {
            "field_id": 1,
            "rows": [
                {"name": "fg_category2_name.row", "oid": 1, "type": "terms"},
                {"name": "fg_category3_name.row", "oid": 2, "type": "terms"}
            ],
            "columns": [
                {"name": "gmv", "oid": 1, "type": "terms"},
                {"name": "month_sale", "type": "terms"}
            ],
            "query": "*",
            "type": 4,

        }
        json = request.get_json(force=True)
        json["type"] = 4  # 强制类型为es类型
        json["query"] = "*"
        print "request json:", dumps(json)
        return dumps(self.manager.preview(**json))
