{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
    <link rel="stylesheet" href="/static/plugin/codemirror/lib/codemirror.css" />
    <link rel="stylesheet" href="/static/plugin/codemirror/theme/material.css" />
{% endblock %}
{% block footer %}
    {{ super() }}
    <script src="/static/plugin/codemirror/lib/codemirror.js"></script>
    <script src="/static/plugin/codemirror/mode/python/python.js"></script>
    <script src="/static/plugin/codemirror/mode/sql/sql.js"></script>
    <script src="/static/js/task/hive_edit.js"></script>
{% endblock %}
{% block content %}
<form class="form-horizontal" action="/datasource/save" method="POST">
    <input type="text" name="id" style="display:none" value="{{data.id}}">
    <input type="text" name="types" style="display:none" value="{{types}}">
    <input type="text" name="module_type" style="display:none" value="task">
    <div class="col-md-12 form-group" >
        <input type="text" class="form-control" name="name" value="{{data.name}}" placeholder='任务名称'>
    </div>
    <div class="col-md-4 form-group" >
        <input type="text" class="form-control datepicker" name="st" value="{{data.st}}" placeholder='开始时间,不写默认立即'>
    </div>
    <div class="col-md-4 form-group" >
        <input type="text" class="form-control datepicker" name="et" value="{{data.et}}" placeholder='结束时间，不写默认永久'>
    </div>
    <div class="col-md-4 form-group" >
        <input type="text" class="form-control" name="cron" value="{{data.cron}}" placeholder='运行规则,默认每天1点运行，00 01 * * *'>
    </div>
    <div class="col-md-12 form-group" >
        <textarea name="sqls" id="sql_editor" class="highed-box-size" placeholder='自定义sql' >{{data.sqls}}</textarea>
    </div>
    <div class="col-md-12 form-group" >
        <input type="text" class="form-control" name="hql_params" value="{{data.hql_params}}" placeholder='用于设置一些hive执行的参数变量'>
    </div>
    <div class="col-md-12 form-group" >
        <input type="text" class="form-control" name="del_where" value="{{data.del_where}}" placeholder='如果希望清空里面数据请输入删除条件'>
    </div>
    <div class="col-md-11 form-group" >
        <input type="text" class="form-control" name="customs" value="{{data.customs}}" placeholder='请输入自定义变量的值'>
    </div>
    <div class="col-md-1 form-group">
        <button type="button" id="sql_show" class="btn btn-info">查看sql</button>
    </div>
    <div class="col-md-12 form-group">
        <span style="color:red;font-size:0.2em">注意：此处变量只支持<strong>时间类型参数(其余参数不支持变更)</strong>;查看sql请点击<strong>查看sql</strong></span>
    </div>
    <div class="col-md-11 form-group"></div>
    <div class="col-md-1 form-group">
        <button type="button" id="submit" class="btn btn-success">Save</button>
    </div>
</form>
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
{% endblock %}
