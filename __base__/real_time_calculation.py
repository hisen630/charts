# coding:utf-8

from mapping import DataSourceMappingBase


class RealTimeCalculationBase(DataSourceMappingBase):
    """ 实时计算基类 """


class RealTimeCalculation(RealTimeCalculationBase):
    def __init__(self, index_or_db="online_taobao_*_*-*-*", type_or_table="item_list",
                 columns=(), rows=(), query="*"):
        self.index_or_db = index_or_db
        self.type_or_table = type_or_table
        self.columns = columns or [u'fg_category2_name.raw__terms', u'fg_category3_name.raw__terms']
        self.rows = rows or [u'gmv__value', u'view_price__value', u'month_sale__value']
        self.query = query


RTC = RealTimeCalculation
