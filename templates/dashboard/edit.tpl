{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
    <link rel="stylesheet" href="/static/plugin/codemirror/lib/codemirror.css" />
    <link rel="stylesheet" href="/static/plugin/codemirror/theme/material.css" />
{% endblock %}
{% block footer %}
    {{ super() }}
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
                    <tr id="datasource_{{item.id}}">
                        <td>{{item.id}}</td>
                        <td>
                            <label>{{item.name}}</label><input type="text" class="form-control" style="display:none" value="{{item.id}}" name="ids">
                        </td>
                        <td>
                            <button type="button" class="btn btn-danger chart_del">删除</button>
                        </td>
                    </tr>
                    {%endfor%}
                </tbody>
            </table>
        </fieldset>
    </div>
    <div class="col-md-12 form-group" >
        <select name="select_charts" class="col-md-10 multiple select_nopad">
            {% for item in datasources %}
                <option value='{{item.id}}' data-conf="{{item.jsons}}">{{item.name}}</option>
            {% endfor %}
        </select>
        <button type="button" id="add_chart" class="col-md-2 btn btn-primary">添加报表</button>
    </div>
    <div class="col-md-12 form-group" >
        <input type="text" class="form-control" name="name" value="{{data.name}}" placeholder='dashboard名称'>
    </div>
    <div class="col-md-2 form-group">
        <button type="button" class="btn btn-info" id="create_notebook">Priview</button>
    </div>
    <div class="col-md-9"></div>
    <div class="col-md-1 form-group">
        <button type="button" id="submit" class="btn btn-success">保存</button>
    </div>
</form>

{% endblock %}
