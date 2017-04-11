# -*- coding: utf-8 -*-
from common.base import render_custom
from flask import abort, redirect, url_for, jsonify
from flask import request
from common.utils import defaultencode
from manager import notebook_m
import json

class Notebook():
    #新建notebook并返回编辑地址
    def new(self):
        result = {'status':1,'msg':u'创建notebook失败'}
        if request.method == 'POST':
            form = request.form.to_dict()
            result = notebook_m.get_notebook(form)
        return json.dumps(result,default=defaultencode)

    #新建notebook并返回编辑地址
    def new_muti(self):
        result = {'status':1,'msg':u'创建notebook失败'}
        if request.method == 'POST':
            result = notebook_m.get_notebook_muti(request.form)
        return json.dumps(result,default=defaultencode)