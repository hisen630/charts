# coding:utf-8
from __base__ import System
from abc import ABCMeta
from mapping import Mapping


class RealTimeCalculationBase(object):
    """ 实时计算基类 """
    __metaclass__ = ABCMeta


class RealTimeCalculation(RealTimeCalculationBase, System):
    """ 实时计算类 """


class RealTimeCalculationMappingBase(RealTimeCalculation, Mapping):
    """ 实时计算基础方法并对应映射层 """


class RealTimeCalculationMapping(RealTimeCalculationMappingBase):
    """ 实时计算实现类统一接口 """
    address = None  # 地址
    rows = ()  # 行／维度
    columns = ()  # 列/指标
    query = "*"  # 查询内容默认为 *

    def __init__(self, address=None, columns=None, rows=None, query=None):
        # field_id, columns = None, rows = None, query = "*", type = 4
        """ 优先使用传入参数，否则使用默认参数 """
        self.address = address or self.address
        self.columns = columns or self.columns
        self.rows = rows or self.rows
        self.query = query or self.query
        assert self.address and self.query  # 索引、类型和query必须存在


RTC = RealTimeCalculationMapping
