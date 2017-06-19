# coding:utf-8

from __base__ import ToolsBase
from json import dumps
from requests import Session


class Client(ToolsBase, Session):
    def request_json(self, *args, **kwargs):
        """ body 为json字符串 请求 """
        return self.request(data=dumps(kwargs.pop("body", "{}")), *args, **kwargs)
