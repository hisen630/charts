# -*- coding: utf-8 -*-
from common.base import render_custom
from flask import abort, redirect, url_for, jsonify
from flask import request
from common.utils import defaultencode
from manager import  datasource_m
from common import mysql_base
from base import base_b
import json

class DataSource():

    #列表页
    def index(self):
        return render_custom('datasource/index.tpl')

    #编辑
    def edit(self):
        data = {}
        types = 0
        if request.method == 'GET':
            cid = request.args.get('id', '')
            types = request.args.get('types', 0)
            types = int(types)
            if cid:
                data = datasource_m.get_datasource(int(cid),True)
                if data:
                    types = data['types']
        modules = base_b.get_modules("datasource",types)
        for item in modules:
            return render_custom(item['template'],data=data,types=types)
        else:
            return render_custom("layouts/developing.tpl",data=data,types=types)

    #保存方法
    def save(self):
        result = {'status':0,'msg':u'请求保存失败'}
        if request.method == 'POST':
            result = datasource_m.save(request.form)
        return jsonify(result)

    #获取数据
    def get_data(self):
        result = {'status':0,'msg':u'获取失败'}
        if request.method == 'POST':
            result = datasource_m.get_data(request.form.to_dict(),rows=10)
        return json.dumps(result,default=defaultencode)

    #获取sql
    def get_sql(self):
        result = {'status':0,'msg':u'获取失败'}
        sqls = ''
        if request.method == 'POST':
            customs = request.form.get('customs','')
            sqls = request.form.get('sqls', '')
        result = mysql_base.get_sql(sqls,customs)
        return json.dumps(result,default=defaultencode)

    def search(self):
        result = {'current':1,'total':0,'rows':[]}
        if request.method == 'POST':
            cid = request.form.get('id', '')
            name = request.form.get('name', '')
            current = request.form.get('current', 1)
            rowCount = request.form.get('rowCount', 20)
            result = datasource_m.get_list(cid,name,current,rowCount)
        return json.dumps(result,default=defaultencode)
