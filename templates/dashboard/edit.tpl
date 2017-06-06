{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
    <link rel="stylesheet" href="/static/plugin/codemirror/lib/codemirror.css" />
    <link rel="stylesheet" href="/static/plugin/codemirror/theme/material.css" />
{% endblock %}
{% block footer %}
    {{ super() }}
    <script src="/static/plugin/md5.js"></script>
    <script src="/static/js/dashboard/edit.js"></script>
{% endblock %}
{% block content %}
<style type="text/css">
fieldset {
    padding:5px;
    margin:5px;
    width:auto;
    color:#333; 
    border:#06c dashed 1px;
} 
legend {
    color:#06c;
    border-bottom:none;
    font-size:15;
    width: auto;
    margin-bottom:auto;
}
ul {
    list-style-type: none;
    margin:auto;
}
</style>
</div>
</div>
<link href="/static/plugin/highchart_edit/highcharts-editor.min.css" type="text/css" rel="stylesheet"/>
<form class="form-horizontal" action="/mysql/save" method="POST">
    <input type="text" name="id" style="display:none" value="{{data.id}}">
    <div class="col-md-12 form-group" >
        <input type="text" class="form-control" name="name" value="{{data.name}}" placeholder='dashboard名称'>
    </div>
    <div class="col-md-12 form-group" >
        <select name="select_charts" class="col-md-10 multiple select_nopad">
            {% for item in datasources %}
                <option value='{{item.id}}' data-conf="{{item.conf}}">{{item.name}}</option>
            {% endfor %}
        </select>
        <button type="button" id="add_chart" class="col-md-2 btn btn-primary">添加报表</button>
    </div>
    <div class="col-md-12 form-group" >
        <label class="col-md-1">name：</label>
        <input type="text" class="col-md-4 form-control" name="input_name" value="" placeholder='iframe名称'>
        <label class="col-md-1">iframe：</label>
        <input type="text" class="col-md-4 form-control" name="input_iframe" value="" placeholder='iframe地址'>
        <button type="button" id="add_chart_iframe" class="col-md-2 btn btn-primary">添加iframe</button>
    </div>
    <div class="col-md-12 form-group">
        <fieldset>
            <legend>数据源</legend>
            <table id="maingrid" class="table table-condensed table-hover table-striped">
                <thead>
                    <tr>
                      <th>数据源id</th>
                      <th>数据源名称</th>
                      <th>操作</th>
                    </tr>
                </thead>
                <tbody id="data_group">
                    {%for item in data.cinfo%}
                    <tr id="chart_{{item.id}}">
                        <td>{{item.id}}</td>
                        <td>
                            <label>{{item.name}}</label><input type="text" class="form-control" style="display:none" value="{{item.value}}" name="ids">
                        </td>
                        <td>
                            <button type='button' class='btn btn-defalut chart_up' title='move up'><span class='glyphicon glyphicon-arrow-up'></span></button>
                            <button type='button' class='btn btn-defalut chart_down' title='move down'><span class='glyphicon glyphicon-arrow-down'></span></button>
                            <button type='button' class='btn btn-defalut chart_del' title='delete'><span class='glyphicon glyphicon-remove'></span></button>
                        </td>
                    </tr>
                    {%endfor%}
                </tbody>
            </table>
        </fieldset>
    </div>
    <div class="col-md-12 form-group">
        <fieldset>
            <legend>全局参数设定</legend>
            <table id="maingrid" class="table table-condensed table-hover table-striped">
                <thead>
                    <tr>
                      <th>参数名称</th>
                      <th>展示类型</th>
                      <th>操作</th>
                    </tr>
                </thead>
                <tbody id="params_group">
                    {%for item in data.globals%}
                    <tr>
                        <td>{{item.params_customs_name}}</td>
                        <td>
                            <label>{% if item.params_types=="0" %}input{%elif item.params_types=="1" %}select{%else%}null{%endif%}</label><input type="text" class="form-control" style="display:none" value='{{item.globals}}' name="search_params">
                        </td>
                        <td>
                            <button type='button' class='btn btn-defalut chart_up' title='move up'><span class='glyphicon glyphicon-arrow-up'></span></button>
                            <button type='button' class='btn btn-defalut chart_down' title='move down'><span class='glyphicon glyphicon-arrow-down'></span></button>
                            <button type='button' class='btn btn-defalut params_edit' title='edit'><span class='glyphicon glyphicon-edit'></span></button>
                            <button type='button' class='btn btn-defalut params_del' title='delete'><span class='glyphicon glyphicon-remove'></span></button>
                        </td>
                    </tr>
                    {%endfor%}
                </tbody>
            </table>
        </fieldset>
    </div>
    <div class="col-md-2 form-group">
    </div>
    <div class="col-md-9"></div>
    <div class="col-md-1 form-group">
        <button type="button" id="submit" class="btn btn-success">保存</button>
    </div>
</form>
<!--  -->
<div class="modal fade" id="params_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
        <h4 class="modal-title">全局参数定义</h4>
      </div>
      <div class="modal-body">
          <div class="form-group">
            <label class="control-label">参数名称：</label>
            <input type="text" class="form-control" name="params_name" placeholder='参数名称'>
          </div>
          <div class="form-group">
            <label class="control-label">参数类型：</label>
            <select name="params_types" class="form-control multiple">
                <option value='0'>input</option>
                <option value='1'>select</option>
            </select>
          </div>
          <div class="form-group">
            <label class="control-label">默认值：</label>
            <input type="text" class="form-control" value="" name="params_default" placeholder='默认值'>
          </div>
          <div class="form-group for_select">
            <label class="control-label">多选个数（单选请填1）：</label>
            <input type="text" class="form-control" value="1" name="params_counts" placeholder='多选个数，请填数字'>
          </div>
          <div class="form-group for_select" class="choose_select">
            <label class="control-label">数据来源(自定义请写name:value;sql请写：mysql连接;sql)：</label>
            <textarea type="text" class="form-control" value="" name="params_datasource" placeholder='如有需要，请按照之前内容自定义'></textarea>
          </div>
          <input type="text" class="form-control" value="" name="params_customs_name" style="display:none">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
        <button type="button" class="btn btn-success submit" data-dismiss="modal">保存</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
{% endblock %}
