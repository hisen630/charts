# -*- coding: utf-8 -*-
from utils import get_py_file
from flask import render_template as render
from flask import request
from manager import menu_m
from conf.default import _modules_name
import os

'''get modules from python file'''
def get_module_object(_modules_split):
    objects = {}
    files = get_py_file("{}/{}/*".format(_modules_name,_modules_split))
    for it in files:
        try:
            tmp = __import__('{}.{}.{}'.format(_modules_name,_modules_split,it),globals(),locals(),[it])
            a = tmp.Manager()
            objects[it] = a
        except Exception, e:
            pass
    return objects

'''add menus to render'''
def render_custom(tpl,**args):
    menus = menu_m.get_menus(request.url)
    return render(tpl,menus=menus,**args)
