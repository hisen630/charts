{% extends "layouts/nav.tpl" %}
{% block header %}
    <link rel="stylesheet" href="/static/plugin/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/plugin/select2/select2.css" />
    <link rel="stylesheet" href="/static/plugin/select2/select2-bootstrap.css" />
    <link rel="stylesheet" href="/static/css/main.css">
    <link href="/static/plugin/metisMenu/metisMenu.min.css" rel="stylesheet">
    <link href="/static/css/sb-admin-2.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/plugin/codemirror/lib/codemirror.css" />
    <link rel="stylesheet" href="/static/plugin/codemirror/theme/material.css" />
{% endblock %}
{% block content %}
    <div style="text-align: center;margin-top:50px ">
    </div>
    <div class="container">
        <div class='row'>
            <form class="form-horizontal" action="/mysql/save" method="POST">
                <input type="text" name="id" style="display:none" value="{{data.id}}">
                <input type="text" name="module_type" style="display:none" value="datasource">
                <div class="col-md-6 form-group" >
                    <input type="text" class="form-control" name="mysql_connect" value="{{data.mysql_connect}}" placeholder='请输入mysql 连接:mysql://root:123456@localhost/metric'>
                </div>
                <div class="col-md-6 form-group" >
                    <input type="text" class="form-control" name="name" value="{{data.name}}" placeholder='报表名称'>
                </div>
                <div class="col-md-12 form-group" >
                    <textarea name="sqls" id="sql_editor" class="highed-box-size" placeholder='自定义sql' >{{data.sqls}}</textarea>
                </div>
                <div class="col-md-11 form-group" >
                    <input type="text" class="form-control" name="custom" value="{{data.custom}}" placeholder='请输入自定义变量的值'>
                </div>
                <div class="col-md-1 form-group">
                    <button type="button" id="sql_show" class="btn btn-info">查看sql</button>
                </div>
                <div class="col-md-12 form-group">
                    <textarea name="code" id="python_editor" class="highed-box-size" placeholder='自定义格式,默认请置空' >{{data.code}}</textarea>
                </div>
                <div class="col-md-2 form-group" style="display:none">
                    <button type="button" id="modal-btn" class="highed-imp-button">chart</button>
                    <input id="chart-result" name="conf" class="highed-box-size" placeholder='配置' value='{{data.conf}}'></input>
                </div>
                <div class="col-md-2 form-group">
                    <button type="button" class="btn btn-info" id="create_notebook">Go to test</button>
                </div>
                <div class="col-md-7 form-group"></div>
                <div class="col-md-2 form-group">
                    <button type="button" id="modal" class="btn btn-info">Create a chart</button>
                </div>
                <div class="col-md-1 form-group">
                    <button type="button" id="submit" class="btn btn-success">Save</button>
                </div>
            </form>
            <div class="col-md-12" id="chart"></div>
        </div>
    </div>
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
        <h4 class="modal-title">Sql</h4>
      </div>
      <div class="modal-body">
        <label id="sql_content" style="width:100%;height:100%"></label>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->

    <script src="/static/plugin/jquery.min.js"></script>
    <script src="/static/plugin/metisMenu/metisMenu.min.js"></script>
    <script src="/static/js/base/sb-admin-2.js"></script>
    <script src="/static/plugin/bootstrap/js/bootstrap.min.js"></script>
    <script src="/static/plugin/select2/select2.min.js"></script>
    <script src="/static/plugin/select2/select2_locale_zh-CN.js"></script>
    <script src="/static/plugin/codemirror/lib/codemirror.js"></script>
    <script src="/static/plugin/codemirror/mode/python/python.js"></script>
    <script src="/static/plugin/codemirror/mode/sql/sql.js"></script>
    <script src="/static/js/datasource/mysql_edit.js"></script>
{% endblock %}