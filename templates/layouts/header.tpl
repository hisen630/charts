<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/static/images/favicon.ico">
    <title>{% block title %}{% endblock %}Seal</title>
    <link rel="stylesheet" href="/static/plugin/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/plugin/select2/select2.css" />
    <link rel="stylesheet" href="/static/plugin/select2/select2-bootstrap.css" />
    <link rel="stylesheet" href="/static/css/main.css">
    <link href="/static/plugin/metisMenu/metisMenu.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/plugin/datetimepicker/bootstrap-datetimepicker.min.css" />
    <link href="/static/css/sb-admin-2.css" rel="stylesheet">
    <link href="/static/plugin/metisMenu/demo.css" rel="stylesheet">
    {% block header %}
    {% endblock %}
</head>
<body>
<div id="wrapper">
{% block nav %}{% endblock %}
<div id="page-wrapper">
    <div class="row">
        <div class="col-lg-12">
            {% block bread_crumbs %}
            {% endblock %}
        </div>
        <div class="col-lg-12">
            {% block content %}
            {% endblock %}
        </div>
    </div>
</div>
</div>
</body>
{% block footer %}
    <script src="/static/plugin/jquery.min.js"></script>
    <script src="/static/plugin/metisMenu/metisMenu.min.js"></script>
    <script src="/static/js/base/sb-admin-2.js"></script>
    <script src="/static/plugin/bootstrap/js/bootstrap.min.js"></script>
    <script src="/static/plugin/select2/select2.min.js"></script>
    <script src="/static/plugin/select2/select2_locale_zh-CN.js"></script>
    <script src="/static/plugin/datetimepicker/bootstrap-datetimepicker.min.js"></script>
    <script src="/static/plugin/datetimepicker/bootstrap-datetimepicker.zh-CN.js"></script>
{% endblock %}