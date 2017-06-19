# -*- coding: utf-8 -*-
from json import dumps
from manager import menu_m
from utils import get_py_file
from web.utils import IterBetter
from conf.default import MODULES_NAME
from flask import request, render_template as render

'''get modules from python file'''


def get_module_object(_modules_split, modules=MODULES_NAME):
    objects = {}
    files = get_py_file("{}/{}/*".format(modules, _modules_split))
    for it in files:
        try:
            tmp = __import__('{}.{}.{}'.format(modules, _modules_split, it), globals(), locals(), [it])
            a = tmp.Manager()
            objects[it] = a
        except Exception, e:
            pass
    return objects


'''add menus to render'''


def render_custom(tpl, **args):
    menus = menu_m.get_menus(request.url)
    return render(tpl, menus=menus, **args)


def jsonify(*args, **kwargs):
    """ 序列化JSON 同时支持对 web—py query后返回的封装对象"""

    def default(items):
        if isinstance(items, IterBetter):
            return [item for item in items]
        return str(items)

    return dumps(default=kwargs.pop("default", default), *args, **kwargs)
