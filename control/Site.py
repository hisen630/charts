# -*- coding: utf-8 -*-
from common.base import render_custom
from flask import abort, redirect, url_for, jsonify
from flask import request
from route import CustomView

class Site(CustomView):
    def index(self):
        return redirect(url_for("/chart/index"))
	def edit(self):
		return render_custom('index.tpl')