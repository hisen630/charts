{% extends "layouts/nav.tpl" %}
{% block head %}
    {{ super() }}
    <link href="/static/plugin/bootgrid/jquery.bootgrid.min.css" type="text/css" rel="stylesheet"/>
{% endblock %}
{% block footer %}
    {{ super() }}
    <script src="/static/plugin/bootgrid/jquery.bootgrid.min.js"></script>
    <script src="/static/js/task/run_index.js"></script>
{% endblock %}
{% block content %}
    <form class="form-vertical" id="mainform">
      <div class="panel panel-default container-fluid" style="margin: 10px 0 10px 0; padding: 10px;">
        <div class="row">
          <div class="col-md-3 form-group">
            <label class="control-label">任务id：</label>
            <input type"text" id="id" name="id" value="{{ tid }}">
          </div>
          <div class="col-md-3 form-group">
            <label class="control-label">任务名称：</label>
            <input type"text" id="name" name="name" value="{{ name }}">
          </div>
          <div class="col-md-5"></div>
          <div class="col-md-1">
            <button type="button" id="search_btn" class="form-control btn btn-success btn-block">搜索</button>
          </div>
        </div>
        </div>
      </div>
    </form>
    <!-- main table -->
    <table id="maingrid" class="table table-condensed table-hover table-striped">
      <thead>
        <tr>
          <th data-column-id="name" data-width="auto">任务名称</th>
          <th data-column-id="types" data-formatter="types" data-width="auto">任务类型</th>
          <th data-column-id="run_time" data-width="auto">指定时间</th>
          <th data-column-id="st" data-width="auto">开始时间</th>
          <th data-column-id="et" data-width="auto">结束时间</th>
          <th data-column-id="status" data-formatter="status" data-width="auto">状态</th>
          <th data-column-id="msg" data-width="auto">信息</th>
          <th data-column-id="commands" data-formatter="commands" data-sortable="false">操作</th>
        </tr>
      </thead>
    </table>
{% endblock %}