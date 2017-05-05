highed.ready(function () {
    a = highed.ModalEditor('highchart_modal',{
        allowDone: true,
        features: 'import templates customize done',
        importer: {
            options: 'csv',
        }
    }, function (obj) {
        json = obj.export.json()
        nowjson = JSON.parse(JSON.stringify(json));
        series = json.series;
        for(key in series){
            if(series[key].hasOwnProperty('data')&&series[key]['data'] && typeof series[key]['data']==='object' &&
            Array == series[key]['data'].constructor){
                len = series[key]['data'].length;
                for(it in series[key]['data']){
                    if(series[key]['data'][it][0]!="-"){
                        tmp = series[key]['data'][it];
                        series[key]['data'] = new Array();
                        series[key]['data'].push(tmp);
                        break;
                    }
                }
            }
        }
        json.series = series;
        highed.dom.get('chart-result').value = JSON.stringify(json);
        Highcharts.chart('chart_show',nowjson);
    });
});
$(function(){
    $(".multiple").select2({
        minimumResultsForSearch:1
    })
    var chart_dom = $(".highed-container").find(".tab-body-padded:first")
    var chart_dom_json = $(".highed-container").find(".tab-body-padded:eq(1)")
    chart_dom.find(".highed-imp-pastearea").attr("disabled","disabled");
    chart_dom.find(".highed-imp-input").attr("disabled","disabled");
    chart_dom.find(".highed-imp-input:eq(2)").val('');
    chart_dom.find(".highed-imp-button:first").attr("display","none");
    //获取数据
    $("#transfer_highchart,#view_result").on("click",function(){
        $("#python_editor").text(python_editor.getValue());
        params = $(".form-horizontal").serialize();
        this_id = $(this).attr("id")
        params['conf'] = ''
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/chart/get_data',
            timeout:20000,
            dataType:"json",
            async:false,
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    $("#data_show").children().remove()
                    $("#chart_show").children().remove()
                    if(this_id=="transfer_highchart"){
                        tmp_sum = new Array();
                        for(item in data.data){
                            tmp_sum.push(data.data[item].join(","));
                        }
                        tmp_sum = tmp_sum.join("\n")
                        chart_dom.find(".highed-imp-pastearea").val(tmp_sum);
                        $("#highchart_modal").click();
                        var json=$("#chart-result").val();
                        chart_dom_json.find(".highed-imp-pastearea").val(json);
                        chart_dom_json.find(".highed-imp-button:eq(1)").click();
                        chart_dom.find(".highed-imp-button:eq(1)").click();
                    }else if(this_id=="view_result"){
                        html = new Array()
                        html.push('<table class="table table-condensed table-hover table-striped">')
                        for(item in data.data){
                            tmp = data.data[item]
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
                        $("#data_show").append(html.join(""))
                    }
                }else{
                    alert(data.msg);
                }
            }
        });
    })
    //获取数据
    $("#view_result").on("click",function(){
        $("#python_editor").text(python_editor.getValue());
        params = $(".form-horizontal").serialize();
        params['conf'] = ''
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/chart/get_data',
            timeout:20000,
            dataType:"json",
            async:false,
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    tmp_sum = new Array();
                    for(item in data.data){
                        tmp_sum.push(data.data[item].join(","));
                    }
                    
                }else{
                    alert(data.msg);
                }
            }
        });
    })
    //保存内容
    $("#submit").on("click",function(){
        $("#python_editor").text(python_editor.getValue());
        params = $(".form-horizontal").serialize();
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/chart/save',
            timeout:20000,
            dataType:"json",
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    alert(data.msg)
                    window.location.href = "/chart/edit?id="+data.data
                }else{
                    alert(data.msg)
                }
            }
        });
    });
    $("#create_notebook").click(function(){
        $("#python_editor").text(python_editor.getValue());
        params = $(".form-horizontal").serialize();
        types = $("form").find("input[name=types]")
        $.ajax({
            type: "POST",
            url:'/notebook/new_muti',
            timeout:20000,
            dataType:"json",
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    window.open(data.data)
                }else{
                    alert(data.msg)
                }
            }
        });
    });
    json = $("#chart-result").val()
    if(json){
        if($("select[name=chart_type]").val()=="0"){
            json = unescape(json)
            json = JSON.parse(json);
            Highcharts.chart('chart_show',json);
        }else if($("select[name=chart_type]").val()=="1"){
            $("#view_result").click()
        }
    }else{
        if($("select[name=chart_type]").val()=="1"){
            $("#view_result").click()
        }
    }
    $("#add_datasource").on("click",function(){
        sid = $("select[name=nouse_datasource]").val()
        options = $("select[name=nouse_datasource]").find("option[value='"+sid+"']")
        types = options.data('types')
        conf = options.data('conf')
        if(types=='0'){
            mysql_modal(types,conf)
        }else if(types=='1'){
            mysql_caculate_modal(types,conf)
        }else if(types=='2'){
            mysql_caculate_modal(types,conf)
        }
    })
    $("select[name=chart_type]").on("change",function(){
        chart_type = $("select[name=chart_type]").val()
        if(chart_type == "1"){
            $("#chart_show").attr("style","")
            $("#view_result").attr("style","")
            $("#transfer_highchart").attr("style","display:none")
        }else{
            $("#chart_show").attr("style","height:400px")
            $("#view_result").attr("style","display:none")
            $("#transfer_highchart").attr("style","")
        }
    })
    $(".modal-dialog .submit").on("click",function(){
        obj = $(this).parents(".modal-dialog")
        types = obj.find("input[name=conf]").data('types')
        if(types=='0'){
            mysql_modal_save(obj)
        }else if(types=='1'){
            mysql_caculate_modal_save(obj)
        }else if(types=='2'){
            mysql_caculate_modal_save(obj)
        }
        
    })
    datasource_on_click()
})

function datasource_on_click(){
    $("button[class*=datasource_edit]").on("click",function(){
        conf = $(this).data("conf")
        if(typeof(conf) == 'string' ){
            conf = unescape(conf)
            conf = JSON.parse(conf)
        }
        customs = $(this).data("customs")
        mysql_modal(conf.types,conf,customs)
    })
    $("button[class*=datasource_del]").on("click",function(){
        $(this).parents("tr").remove()
    })
}

function write_datasource_html(name,customs,conf){
    tmp_conf = unescape(conf)
    conf_obj = JSON.parse(tmp_conf)
    obj = $("#data_group").find("#datasource_"+conf_obj.id)
    if(obj.length){
        obj.find("input[name=customs]").val(customs)
        obj.find("input[name=ids]").val(conf_obj.id)
        obj.find(".datasource_edit").data("customs",customs)
        obj.find(".datasource_edit").data("conf",conf)
    }else{
        html = new Array()
        html.push("<tr id='datasource_"+conf_obj.id+"'>")
        html.push("<td>"+conf_obj.id+"</td>")
        html.push("<td><label>"+name+"</label><input type='text' class='form-control' style='display:none' value='"+customs+"' name='customs'><input type='text' class='form-control' style='display:none' value='"+conf_obj.id+"' name='ids'></td>")
        html.push("<td><button type='button' class='btn btn-success datasource_edit' data-customs='"+customs+"' data-conf=\""+conf+"\">编辑</button><button type='button' class='btn btn-danger datasource_del'>删除</button></td>")
        html.push("</tr>")
        $("#data_group").append(html.join(""))
        datasource_on_click()
    }
}

var python_editor = CodeMirror.fromTextArea(document.getElementById("python_editor"), {
    mode: {
        name: "python",
        version: 2,
        singleLineStringErrors: false
    },
    lineNumbers: true,
    foldGutter: true,
    indentUnit: 4,
    matchBrackets: true,
    theme: "material"
});
