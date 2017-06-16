# coding:utf-8
from sys import stdout
from conf.default import LOG_LEVEL
from logging import basicConfig, root as logger

FORMAT = "[%(asctime)s - %(levelname)s]: %(message)s"
basicConfig(level=LOG_LEVEL, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', stream=stdout)
