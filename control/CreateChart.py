from route import CustomView
from flask import request
from manager.create_chart_m import CreateChartManager
from json import dumps


class CreateChart(CustomView):
    def __init__(self):
        self.manager = CreateChartManager()

    def preview(self):
        args = dict(request.form.to_dict(), **request.args.to_dict())
        args = [args.pop(name) for name in ("field_id", "column_name", "oper_id")]
        return dumps(self.manager.preview(*args))
