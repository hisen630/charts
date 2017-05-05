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
        chart_type = $("#chart").data("types")
        if(conf!=''||conf!=undifined){
            if(chart_type==0){
                $('#chart').highcharts(conf);
            }else{
                html = new Array()
                html.push('<table class="table table-condensed table-hover table-striped">')
                for(item in conf){
                    tmp = conf[item]
                    if(item==0){
                        html.push('<thead>')
                    }
                    html.push('<tr>')
                    for(it in tmp){
                        if(item == 0){
                            html.push("<th>"+tmp[it]+"</th>")
                        }else{
                            html.push("<td>"+tmp[it]+"</td>")
                        }
                    }
                    html.push('</tr>')
                    if(item==0){
                        html.push('</thead><tbody>')
                    }
                }
                html.push('</tbody></table>')
                $("#chart").append(html.join(""))
            }
        }else{
            alert("无配置")
        }
    })
</script>
{% endblock %}
{% block content %}
<div class='row'>
    <div class="col-md-12" id="chart" data-conf='{{data.data}}' data-types='{{data.chart_type}}'></div>
</div>
{% endblock %}
