# coding:utf-8
from __future__ import unicode_literals


class ChartsBaseException(BaseException):
    """ Charts 错误基类 """


class ChartsException(Exception):
    """ 错误类 """
    status = False
    code = 0
    msg = "Charts Error."


class ChartsRequestParamsError(ChartsException):
    """ 请求参数错误 """
    code = 200


if __name__ == '__main__':
    try:
        raise ChartsRequestParamsError("这里是错误提示")
    except ChartsException, e:
        print e.message, e.code, e.status

    TEST_ERROR = ChartsException("测试错误")

    try:
        raise TEST_ERROR
    except ChartsException, e:
        print e.message, e.code, e.status
