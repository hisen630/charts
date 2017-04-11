{% extends "layouts/nav.tpl" %}
{% block head %}
    {{ super() }}
    <link href="/static/plugin/bootgrid/jquery.bootgrid.min.css" type="text/css" rel="stylesheet"/>
{% endblock %}
{% block footer %}
    {{ super() }}
    <script src="/static/plugin/bootgrid/jquery.bootgrid.min.js"></script>
    <script src="/static/js/task/index.js"></script>
{% endblock %}
{% block content %}
    <form class="form-vertical" id="mainform">
      <div class="panel panel-default container-fluid" style="margin: 10px 0 10px 0; padding: 10px;">
        <div class="row">
          <div class="col-md-3 form-group">
            <label class="control-label">任务id：</label>
            <input type"text" id="id" name="id" value="{{ id }}">
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
          <th data-column-id="id" data-type="numeric" data-identifier="true" data-width="auto">#</th>
          <th data-column-id="name" data-width="auto">任务名称</th>
          <th data-column-id="types" data-formatter="types" data-width="auto">任务类型</th>
          <th data-column-id="commands" data-formatter="commands" data-sortable="false">操作</th>
        </tr>
      </thead>
    </table>

<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
        <h4 class="modal-title">手动执行任务</h4>
      </div>
      <div class="modal-body">
         <div class="form-group">
            <label class="control-label">数据源名称：</label>
            <input type="text" class="form-control" value="" name="name" placeholder='数据源名称' disabled="disabled">
          </div>
          <div class="form-group">
            <label class="control-label">指定运行时间：</label>
            <input type="text" class="form-control datepicker" value="" name="custom_time" placeholder='默认为当前时间，通常在有时间变量时使用'>
          </div>
          <input type="text" class="form-control" value="" name="id" style="display:none">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-success submit" data-dismiss="modal">Run</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
{% endblock %}