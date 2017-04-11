# -*- coding: utf-8 -*-
from flask import Flask
from route import Route
from flask import abort, redirect, url_for, jsonify
from common.base import render_custom
app = Flask(__name__)
_Dir = "control"
Route(app,_Dir).build()
@app.route('/')
def index():
    return render_custom("index.tpl")
	# return redirect(url_for("/site/index"))

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=16688, debug=True)
