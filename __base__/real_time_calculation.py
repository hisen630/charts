# coding:utf-8
from abc import ABCMeta
from mapping import Mapping


class RealTimeCalculationBase(object):
    """ 实时计算基类 """
    __metaclass__ = ABCMeta


class RealTimeCalculation(RealTimeCalculationBase):
    """ 实时计算类 """


class RealTimeCalculationMappingBase(RealTimeCalculation, Mapping):
    """ 实时计算基础方法并对应映射层 """


class RealTimeCalculationMapping(RealTimeCalculationMappingBase):
    """ 实时计算实现类统一接口 """
    index_or_db = None  # 索引/数据库
    type_or_table = None  # 类型/表
    rows = ()  # 行／维度
    columns = ()  # 列/指标
    query = "*"  # 查询内容默认为 *

    def __init__(self, index_or_db=index_or_db, type_or_table=type_or_table,
                 columns=columns, rows=rows, query=query):
        """ 优先使用传入参数，否则使用默认参数 """
        assert index_or_db and type_or_table and query  # 索引、类型和query必须存在
        self.index_or_db = index_or_db
        self.type_or_table = type_or_table
        self.columns = columns
        self.rows = rows
        self.query = query


RTC = RealTimeCalculationMapping
