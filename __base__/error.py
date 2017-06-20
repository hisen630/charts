# coding:utf-8
from __future__ import unicode_literals
from __base__ import System
from abc import ABCMeta, abstractproperty


class SystemBaseException(BaseException):
    """ BaseException 错误基类 """


class SystemException(Exception):
    """ Exception 错误基类 """
    __metaclass__ = ABCMeta


class SystemError(SystemException, System):
    """ 错误类 """
    status = abstractproperty()
    code = abstractproperty()
    msg = None


class ChartsError(SystemError):
    """ 错误实现类 """
    status = False
    code = 0
    msg = "Charts Error."

    def __init__(self, message=msg, code=None, *args):
        super(ChartsError, self).__init__(message, *args)
        self.code = code or self.code


class NotImplementedManagerMappingTypeError(ChartsError):
    code = 1001
    msg = "未实现的映射管理器错误(该类型不支持，请修改Type)."


if __name__ == '__main__':

    def test_error(error_object):
        try:
            raise error_object
        except ChartsError, e:
            print e.status, e.code, e.message


    class ChartsRequestParamsError(ChartsError):
        """ 请求参数错误 """
        code = 400


    TEST_ERROR = ChartsError("测试错误", 200)

    test_error(ChartsRequestParamsError("这里是错误提示"))
    test_error(TEST_ERROR)
    test_error(ChartsError())
