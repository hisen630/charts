# coding:utf-8
from sys import stdout
from conf.default import LOG_LEVEL, debug
from logging import basicConfig, root as logger

FORMAT = "[%(asctime)s - %(levelname)s]: %(message)s"
basicConfig(level=LOG_LEVEL, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', stream=stdout)


def _print(*args, **kwargs):
    """ 调试方法 前后虚线隔开"""
    if debug:
        logger.debug("=" * 79)
        logger.debug(*args, **kwargs)
        logger.debug("=" * 79)


logger._print = _print
