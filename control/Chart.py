# -*- coding: utf-8 -*-
from common.base import render_custom
from flask import abort, redirect, url_for, jsonify
from flask import request
from common.utils import defaultencode
from manager import chart_m
import json

class Chart():

    #列表页
    def index(self):
        return render_custom('chart/index.tpl')

    #编辑
    def edit(self):
        data = {}
        datasources = chart_m.get_datasource_list()
        if request.method == 'GET':
            cid = request.args.get('id', '')
            if cid:
                data = chart_m.get_edit(int(cid))
        return render_custom('chart/edit.tpl',data=data,datasources=datasources)

    #保存方法
    def save(self):
        result = {'status':0,'msg':u'请求方法错误'}
        if request.method == 'POST':
            result = chart_m.save(request.form)
        return jsonify(result)

    #获取图表
    def get_chart(self):
        result = {'status':0,'msg':u'获取失败'}
        if request.method == 'GET':
            cid = request.args.get('id', '')
            ajax = request.args.get('ajax', False)
            customs = request.args.get('customs', '')
            if ajax:
                if ajax == 'true':
                    ajax = True
                else:
                    ajax = False
            if cid:
                if customs:
                    try:
                        customs = json.loads(customs)
                    except Exception, e:
                        return {'status':0,'msg':u'自定义参数格式错误，请输入类似[{"3": ""}]'}
                result = chart_m.get_chart(int(cid),customs)
                if result['status'] == 0:
                    return json.dumps(result,default=defaultencode)
            if ajax:
                return json.dumps(result,default=defaultencode)
            else:
                return render_custom('chart/get_chart.tpl',data=result)
        return jsonify(result)

    #获取数据
    def get_data(self):
        result = {'status':0,'msg':u'获取失败'}
        if request.method == 'POST':
            result = chart_m.get_data_by_form(request.form)
        return json.dumps(result,default=defaultencode)

    def search(self):
        result = {'current':1,'total':0,'rows':[]}
        if request.method == 'POST':
            cid = request.form.get('id', '')
            name = request.form.get('name', '')
            current = request.form.get('current', 1)
            rowCount = request.form.get('rowCount', 20)
            result = chart_m.get_list(cid,name,current,rowCount)
        return json.dumps(result,default=defaultencode)
