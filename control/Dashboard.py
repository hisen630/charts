# -*- coding: utf-8 -*-
from common.base import render_custom
from route import CustomView
from flask import abort, redirect, url_for, jsonify
from flask import request
from common.utils import defaultencode
from manager import dashboard_m
import json

class Dashboard(CustomView):

    #列表页
    def index(self):
        return render_custom('dashboard/index.tpl')

    #编辑
    def edit(self):
        data = {}
        datasources = dashboard_m.get_chart_list()
        if request.method == 'GET':
            cid = request.args.get('id', '')
            if cid:
                data = dashboard_m.get_edit(int(cid))
        return render_custom('dashboard/edit.tpl',data=data,datasources=datasources)

    #保存方法
    def save(self):
        result = {'status':0,'msg':u'请求方法错误'}
        if request.method == 'POST':
            result = dashboard_m.save(request.form)
        return jsonify(result)

    #获取图表
    def get_chart(self):
        result = {'status':0,'msg':u'获取失败'}
        if request.method == 'GET':
            cid = request.args.get('id', '')
            ajax = request.args.get('ajax', False)
            istable = request.args.get('istable', False)
            customs = request.args.get('customs', '')
            if ajax:
                if ajax == 'true':
                    ajax = True
                else:
                    ajax = False
            if istable:
                if istable.lower() == 'true':
                    istable = True
                else:
                    istable = False
            if cid:
                if customs:
                    try:
                        customs = json.loads(customs)
                    except Exception, e:
                        return {'status':0,'msg':u'自定义参数格式错误，请输入类似[{"3": {"2":""}}],依次是报表id，数据源id ，数据源自定义参数'}
                result = dashboard_m.get_chart(int(cid),customs,istable=istable)
                if result['status'] == 0:
                    return json.dumps(result,default=defaultencode)
            if ajax:
                return json.dumps(result,default=defaultencode)
            else:
                return render_custom('dashboard/get_chart.tpl',data=result,searchForMat=json.dumps(result['search']))
        return jsonify(result)

    #获取数据
    def priview(self):
        result = {'status':0,'msg':u'获取失败'}
        if request.method == 'GET':
            result = dashboard_m.get_data_by_form(request.form)
        return json.dumps(result,default=defaultencode)

    def search(self):
        result = {'current':1,'total':0,'rows':[]}
        if request.method == 'POST':
            did = request.form.get('id', '')
            name = request.form.get('name', '')
            current = request.form.get('current', 1)
            rowCount = request.form.get('rowCount', 20)
            result = dashboard_m.get_list(did,name,current,rowCount)
        return json.dumps(result,default=defaultencode)
