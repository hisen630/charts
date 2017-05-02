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
    <script src="/static/js/datasource/hive_edit.js"></script>
{% endblock %}
{% block content %}
<form class="form-horizontal" action="/datasource/save" method="POST">
    <input type="text" name="id" style="display:none" value="{{data.id}}">
    <input type="text" name="types" style="display:none" value="{{types}}">
    <input type="text" name="module_type" style="display:none" value="datasource">
    <div class="col-md-12 form-group" >
        <input type="text" class="form-control" name="name" value="{{data.name}}" placeholder='数据源名称'>
    </div>
    <div class="form-group" >
        <label class="col-md-1 control-label">任务</label>
        <select name="tid" class="multiple col-md-10" >
            {% for item in data.tasks %}
                <option value='{{item.id}}' data-tables='{{item.table_infos}}' {% if item.id==data.tid %}checked{%endif%} >{{item.name}}</option>
            {% endfor %}
        </select>
    </div>
    <div class="col-md-12 form-group" >
        <textarea name="sqls" id="sql_editor" class="highed-box-size" placeholder='自定义sql:select * from task_table limit 10;' >{% if data.sqls %}{{data.sqls}}{%else%}select * from task_table limit 10;{%endif%}</textarea>
    </div>
    <div class="col-md-11 form-group" >
        <span style="color:red;font-size:0.2em">注意：表名统一写成<strong>task_table</strong>，它会自动替代任务的结果表;当需要指定task_table的alias时不用使用as,系统默认指定为<strong>_alias</strong>(example:select * from task_table left join some b on _alias.id=b.id);查看字段请点击<strong>view result</strong></span>
    </div>
    <div class="col-md-11 form-group" >
        <input type="text" class="form-control" name="customs" value="{{data.customs}}" placeholder='请输入自定义变量的值'>
    </div>
    <div class="col-md-1 form-group">
        <button type="button" id="sql_show" class="btn btn-info">查看sql</button>
    </div>
    <div class="col-md-12 form-group">
        <textarea name="code" id="python_editor" placeholder='自定义格式,默认请置空' >{{data.code}}</textarea>
    </div>
    <div class="col-md-2 form-group">
        <button type="button" class="btn btn-info" id="create_notebook">Go to notebook</button>
    </div>
    <div class="col-md-2 form-group">
        <button type="button" class="btn btn-info" id="view_result">view result</button>
    </div>
    <div class="col-md-7 form-group"></div>
    <div class="col-md-1 form-group">
        <button type="button" id="submit" class="btn btn-success">Save</button>
    </div>
</form>
<div class="col-md-12" id="data_show"></div>
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
