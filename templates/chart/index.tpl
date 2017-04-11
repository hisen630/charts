{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
    <link href="/static/plugin/bootgrid/jquery.bootgrid.min.css" type="text/css" rel="stylesheet"/>
{% endblock %}
{% block footer %}
    {{ super() }}
    <script src="/static/plugin/bootgrid/jquery.bootgrid.min.js"></script>
    <script src="/static/js/chart/index.js"></script>
{% endblock %}
{% block content %}
    <form class="form-vertical" id="mainform">
      <div class="panel panel-default container-fluid" style="margin: 10px 0 10px 0; padding: 10px;">
        <div class="row">
          <div class="col-md-3 form-group">
            <label class="control-label">图表id：</label>
            <input type"text" id="id" name="id" value="{{ id }}">
          </div>
          <div class="col-md-3 form-group">
            <label class="control-label">图表名称：</label>
            <input type"text" id="name" name="name" value="{{ name }}">
          </div>
          <div class="col-md-1">
            <button type="button" id="search_btn" class="form-control btn btn-success btn-block">查询</button>
          </div>
          <div class="col-md-1">
            <a type="button" href="/chart/edit" target="_blank" class="form-control btn btn-success btn-block">新增</a>
          </div>
        </div>
        </div>
      </div>
    </form>
    <!-- main table -->
    <table id="maingrid" class="table table-condensed table-hover table-striped">
      <thead>
        <tr>
          <th data-column-id="id" data-type="numeric" data-identifier="true" data-width="auto">#</th>
          <th data-column-id="name" data-width="auto">图表名称</th>
          <th data-column-id="commands" data-formatter="commands" data-sortable="false">操作</th>
        </tr>
      </thead>
    </table>
{% endblock %}