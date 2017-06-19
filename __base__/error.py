# coding:utf-8
from __future__ import unicode_literals
from abc import ABCMeta


class SystemBaseExceptionBase(BaseException):
    """ Charts 错误基类 """


class SystemExceptionBase(Exception):
    """ 错误类 """
    __metaclass__ = ABCMeta


class ChartsException(SystemExceptionBase):
    """ 错误实现类 """
    status = False
    code = 0
    msg = "Charts Error."


if __name__ == '__main__':
    class ChartsRequestParamsError(ChartsException):
        """ 请求参数错误 """
        code = 400


    try:
        raise ChartsRequestParamsError("这里是错误提示")
    except ChartsException, e:
        print e.message, e.code, e.status

    TEST_ERROR = ChartsException("测试错误")

    try:
        raise TEST_ERROR
    except ChartsException, e:
        print e.message, e.code, e.status
