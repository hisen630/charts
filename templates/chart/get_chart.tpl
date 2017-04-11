{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
{% endblock %}
{% block footer %}
    {{ super() }}
    <script src="/static/plugin/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
<script type="text/javascript">
    $(function () {
        conf = $("#chart").data("conf")
        if(conf!=''||conf!=undifined){
            $('#chart').highcharts(conf);
        }else{
            alert("无配置")
        }
    })
</script>
{% endblock %}
{% block content %}
<div class='row'>
    <div class="col-md-12" id="chart" data-conf='{{data.data}}'></div>
</div>
{% endblock %}
