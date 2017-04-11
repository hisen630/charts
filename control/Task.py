# -*- coding: utf-8 -*-
from common.base import render_custom
from flask import abort, redirect, url_for, jsonify
from flask import request
from common.utils import defaultencode
from manager import  task_m
from common import mysql_base
from base import base_b
import json

class Task():

    #列表页
    def index(self):
        return render_custom('task/index.tpl',task=['1'],pa=['pa'])

    #编辑
    def edit(self):
        data = {}
        types = 0
        if request.method == 'GET':
            cid = request.args.get('id', '')
            types = request.args.get('types', 0)
            types = int(types)
            if cid:
                data = task_m.get_datasource(int(cid),True)
                if data:
                    types = data['types']
        modules = base_b.get_modules("task",types)
        for item in modules:
            return render_custom(item['template'],data=data,types=types)
        else:
            return render_custom("layouts/developing.tpl",data=data,types=types)

    #保存方法
    def save(self):
        result = {'status':0,'msg':u'请求保存失败'}
        if request.method == 'POST':
            result = task_m.save(request.form)
        return jsonify(result)

    #获取数据
    def get_data(self):
        result = {'status':0,'msg':u'获取失败'}
        if request.method == 'POST':
            result = task_m.get_data(request.form.to_dict(),rows=10)
        return json.dumps(result,default=defaultencode)

    #获取sql
    def get_sql(self):
        result = {'status':0,'msg':u'获取失败'}
        if request.method == 'POST':
            customs = request.form.get('customs','')
            sqls = request.form.get('sqls', '')
            hql_params = request.form.get('hql_params', '')
            result = mysql_base.get_sql(sqls,customs,hql_params)
        return json.dumps(result,default=defaultencode)

    #任务列表
    def search(self):
        result = {'current':1,'total':0,'rows':[]}
        if request.method == 'POST':
            cid = request.form.get('id', '')
            name = request.form.get('name', '')
            current = request.form.get('current', 1)
            rowCount = request.form.get('rowCount', 20)
            result = task_m.get_list(cid,name,current,rowCount)
        return json.dumps(result,default=defaultencode)

    #列表页
    def run_index(self):
        tid = ""
        name = ""
        if request.method == 'GET':
            tid = request.args.get('tid', '')
            name = request.args.get('name', '')
        return render_custom('task/run_index.tpl',tid=tid,name=name)

    #任务日志
    def run_search(self):
        result = {'current':1,'total':0,'rows':[]}
        if request.method == 'POST':
            cid = request.form.get('id', '')
            name = request.form.get('name', '')
            current = request.form.get('current', 1)
            rowCount = request.form.get('rowCount', 20)
            result = task_m.get_runlog_list(cid,name,current,rowCount)
        return json.dumps(result,default=defaultencode)


    def run_single(self):
        result = {"status":0,"msg":"缺少必要参数"}
        if request.method == 'POST':
            tid = request.form.get('tid', '')
            lid = request.form.get('lid', '')
            custom_time  = request.form.get("custom_time","")
            opertype = request.form.get('opertype', 1)
            result = task_m.run_single(tid,lid,custom_time,opertype)
        return json.dumps(result,default=defaultencode)

    def run_cancel(self):
        result = {"status":0,"msg":"缺少必要参数"}
        if request.method == 'POST':
            lid = request.form.get('lid', '')
            result = task_m.run_cancel(lid)
        return json.dumps(result,default=defaultencode)
