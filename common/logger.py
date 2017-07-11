# coding:utf-8
from sys import stdout
from json import dumps
from types import DictType, ListType
from conf.default import LOG_LEVEL, debug
from logging import basicConfig, root as logger

FORMAT = "[%(asctime)s - %(levelname)s]: %(message)s"
basicConfig(level=LOG_LEVEL, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', stream=stdout)


def pprint(message, *args, **kwargs):
    """ 调试方法 前后虚线隔开"""
    if debug:
        logger.debug("=" * 79)
        if isinstance(message, (DictType, ListType)):
            message = dumps(message, indent=4)
        logger.debug(message, *args, **kwargs)
        logger.debug("=" * 79)


logger.pprint = pprint
