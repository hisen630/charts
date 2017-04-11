{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
    <link rel="stylesheet" href="/static/plugin/codemirror/lib/codemirror.css" />
    <link rel="stylesheet" href="/static/plugin/codemirror/theme/material.css" />
{% endblock %}
{% block footer %}
    {{ super() }}
    <script src="https://code.highcharts.com/stock/highstock.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/adapters/standalone-framework.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/highcharts-more.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/highcharts-3d.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/modules/data.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/funnel.js"></script>
    <script src="https://code.highcharts.com/modules/solid-gauge.js"></script>
    <script src="/static/plugin/highchart_edit/highcharts-editor.min.js"></script>
    <script src="/static/plugin/highchart_edit/highcharts-editor.advanced.min.js"></script>
    <script src="/static/plugin/codemirror/lib/codemirror.js"></script>
    <script src="/static/plugin/codemirror/mode/python/python.js"></script>
    <script src="/static/plugin/codemirror/mode/sql/sql.js"></script>
    <script src="/static/js/chart/add_source_modal.js"></script>
    <script src="/static/js/chart/edit.js"></script>
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
                    {%for item in data.customs%}
                    <tr id="datasource_{{item.id}}">
                        <td>{{item.id}}</td>
                        <td>
                            <label>{{item.conf.name}}</label>
                            <input type="text" class="form-control" style="display:none" value="{{item.customs}}" name="customs"><input type="text" class="form-control" style="display:none" value="{{item.id}}" name="ids">
                        </td>
                        <td>
                            <button type="button" class="btn btn-success datasource_edit" data-customs="{{item.customs}}" data-conf="{{item.json}}">编辑</button>
                            <button type="button" class="btn btn-danger datasource_del">删除</button>
                        </td>
                    </tr>
                    {%endfor%}
                </tbody>
            </table>
        </fieldset>
    </div>
    <div class="form-group" >
        <select name="nouse_datasource" class="col-md-10 multiple" >
            {% for item in datasources %}
                <option value='{{item.id}}' data-types='{{item.types}}' data-conf="{{item.jsons}}">{{item.name}}</option>
            {% endfor %}
        </select>
        <button type="button" id="add_datasource" class="col-md-1 btn btn-primary">添加数据源</button>
    </div>
    <div class="col-md-12 form-group" >
        <input type="text" class="form-control" name="name" value="{{data.name}}" placeholder='报表名称'>
    </div>
    <div class="col-md-12 form-group">
        <textarea name="code" id="python_editor" class="highed-box-size" placeholder='自定义格式,默认请置空:\ndef trans(args):\n    return args[0]' >{{data.code}}</textarea>
    </div>
    <div class="col-md-2 form-group" style="display:none">
        <button type="button" id="highchart_modal" class="highed-imp-button">chart</button>
        <input id="chart-result" name="conf" class="highed-box-size" placeholder='配置' value='{{data.conf}}'></input>
    </div>
    <div class="col-md-2 form-group">
        <button type="button" class="btn btn-info" id="create_notebook">Go to test</button>
    </div>
    <div class="col-md-7 form-group"></div>
    <div class="col-md-2 form-group">
        <button type="button" id="transfer_highchart" class="btn btn-info">Create a chart</button>
    </div>
    <div class="col-md-1 form-group">
        <button type="button" id="submit" class="btn btn-success">保存</button>
    </div>
    <div class="col-md-12" id="chart_show" style="height:400px"></div>
</form>


<!-- mysql 数据源 -->
<div class="modal fade" id="mysql" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
        <h4 class="modal-title">mysql 数据源定义</h4>
      </div>
      <div class="modal-body">
          <div class="form-group">
            <label class="control-label">数据源名称：</label>
            <input type="text" class="form-control" value="" name="name" placeholder='数据源名称' disabled="disabled">
          </div>
          <div class="form-group">
            <label class="control-label">原自定义：</label>
            <input type="text" class="form-control" value="" name="old_customs" placeholder='原自定义' disabled="disabled">
          </div>
          <div class="form-group">
            <label class="control-label">自定义：</label>
            <input type="text" class="form-control" value="" name="customs" placeholder='如有需要，请按照之前内容自定义'>
          </div>
          <input type="text" class="form-control" value="" data-types="" name="conf" style="display:none">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
        <button type="button" class="btn btn-success submit" data-dismiss="modal">添加</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
{% endblock %}
