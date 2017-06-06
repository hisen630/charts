{% extends "layouts/search.tpl" %}
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
                if(conf['status']==1&&conf.hasOwnProperty("data")){
                    data = JSON.parse(conf['data'])
                    if(conf['chart_type']==0){
                        $('#obj_'+cid).highcharts(data);
                    }else if(conf['chart_type']==-1){
                        html = new Array()
                        html.push('<iframe src="'+data['url'].replace(/’/g,"'")+'" height="400" width="100%"></iframe>')
                        $('#obj_'+cid).append(html.join(""))
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
    var parseParam=function(param, key){
        var paramStr="";
        if(param instanceof String||param instanceof Number||param instanceof Boolean){
            paramStr+="&"+key+"="+encodeURIComponent(param);
        }else{
            $.each(param,function(i){
                var k=key==null?i:key+(param instanceof Array?"["+i+"]":"."+i);
                paramStr+='&'+parseParam(this, k);
            });
        }
        return paramStr.substr(1);
    };
    $("button[class*=submit]").on("click",function(){
        seachform = $("#Searchform").serializeArray()
        params = {}
        for(item in seachform){
            is_select_mutiple = endwith(seachform[item]['name'],"\\[\]")
            name = seachform[item]['name']
            if(is_select_mutiple){
                name = seachform[item]['name'].replace("\[\]","")
            }
            if(seachform[item]['value'].replace(/(^s*)|(s*$)/g, "").length>0){
                if(params.hasOwnProperty(name)){
                    params[name].push(seachform[item]['value'])
                }else{
                    params[name] = new Array()
                    params[name].push(seachform[item]['value'])
                }
            }
        }
        params_result = new Array()
        for(item in params){
            params_result.push(item+":"+params[item])
        }
        params_result = params_result.join(";")
        params_result = params_result.replace("\"","\\\"")
        now_params = getUrlArgObject()
        now_params["customs"] = '{"0":{"customs":"'+params_result+'"}}'
        url = window.location.origin+window.location.pathname+"?"+parseParam(now_params)
        window.location.href=url
    })

function endwith(string,str){
    return new RegExp(str+"$").test(string)
}

//返回的是对象形式的参数    
function getUrlArgObject(){    
    var args=new Object();    
    var query=location.search.substring(1);//获取查询串    
    var pairs=query.split("&");//在逗号处断开    
    for(var i=0;i<pairs.length;i++){    
        var pos=pairs[i].indexOf('=');//查找name=value    
        if(pos==-1){//如果没有找到就跳过    
            continue;    
        }    
        var argname=pairs[i].substring(0,pos);//提取name    
        var value=pairs[i].substring(pos+1);//提取value    
        args[argname]=unescape(value);//存为属性    
    }    
    return args;//返回对象    
}
</script>
{% endblock %}
{% block content %}
<div class='row' id="chart" data-conf='{{data.data}}'>
</div>
{% endblock %}
