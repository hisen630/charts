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
        json = {
            "field_id": 1,
            "rows": [
                {"name": "gmv", "oid": 1},
                {"name": "month_sale", "oid": 1}
            ],
            "columns": [
                {"name": "fg_category2_name.raw", "oid": 1, "size": 5, "order": "desc"},
                # {"name": "fg_category3_name.raw", "oid": 2, "type": "terms", "size": 5, "order": "ase"}

            ],
            "query": "*",
        }
        # json = request.get_json(force=True)
        json["type"] = 4  # 强制类型为es类型
        json["query"] = "*"
        print "request json:", dumps(json)
        return dumps(self.manager.preview(**json))
