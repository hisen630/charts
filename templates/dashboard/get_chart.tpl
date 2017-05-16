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
        confs = $("#chart").data("conf")
        if(confs!=''||confs!=undifined){
            for(cid in confs){
                conf = confs[cid]
                $("#chart").append('<div class="col-md-12" id="obj_'+cid+'" style="height:400px"></div>')
                if(conf['status']==1){
                    data = JSON.parse(conf['data'])
                    if(conf['chart_type']==0){
                        $('#obj_'+cid).highcharts(data);
                    }else{
                        html = new Array()
                        html.push('<table class="table table-condensed table-hover table-striped">')
                        for(item in data){
                            tmp = data[item]
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
                        $('#obj_'+cid).append(html.join(""))
                    }
                }else{
                    $('#obj_'+cid).append(cid+"报表无数据")
                }
            }
        }else{
            alert("无配置")
        }
    })
</script>
{% endblock %}
{% block content %}
<div class='row' id="chart" data-conf='{{data.data}}'>
</div>
{% endblock %}
