# coding:utf-8
""" 所有抽象类，API的强制方法均在这里汇总，同时可以在这里实现方法
    保证一点：所有实现类需要继承基础类的子类，也就是实现类必须是孙类 
"""
from data import DataBase, Data
from logic import LogicBase, Logic
from tools import ToolsBase, Tools
from control import ControlBase, Control
from manager import ManagerBase, Manager
from notebook import NotebookBase, Notebook
from mapping import MappingBase, Mapping, Mapping1
from config import ConfigBase, Config, ConfigDefault
from task import TaskBase, Task, TaskMappingBase, TaskMapping
from elastic_search import (
    ElasticSearchBase,
    ElasticSearch,
    ElasticSearchParseBase,
    ElasticSearchParse,
    ElasticSearchParamsParse,
    ElasticSearchQuery,
    ElasticSearchAggregation,
    ElasticSearchFiltered,
)

from error import (
    SystemBaseException,
    SystemException,
    SystemError,
    ChartsError,
    APIError,
    AssertionError,
    NotImplementedManagerMappingTypeError,
)

from real_time_calculation import (
    RealTimeCalculationBase,
    RealTimeCalculation,
    RealTimeCalculationMappingBase,
    RealTimeCalculationMapping,
    RTC
)
