# -*- coding: utf-8 -*-
from create_chart.elasticsearch import mappings, range_mappings

mappings = {
    4: {
        "string": {
            "filter": mappings["string"]["filter"].keys(),
        },
        "number": {
            "aggregates": mappings["number"]["aggregation"].keys(),
            "filter": range_mappings.keys(),
        }
    },
}


class DataSource(object):
    """docstring for DataSource"""

    def __init__(self):
        self.types = 0

    def get_datasource_other(self, data):
        return data
