$(function(){
    $(".multiple").select2({
        minimumResultsForSearch:1
    })
    //保存内容
    $("#submit").on("click",function(){
        params = $(".form-horizontal").serialize();
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/dashboard/save',
            timeout:20000,
            dataType:"json",
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    alert(data.msg)
                    window.location.href = "/dashboard/edit?id="+data.data
                }else{
                    alert(data.msg)
                }
            }
        });
    });
    var customs_global = {}
    $("select[name=select_charts]").find("option").each(function(){
        customs_global[$(this).val()]=$(this).data("conf")
    })
    $("#add_chart").on("click",function(){
        cid = $("select[name=select_charts]").val()
        options = $("select[name=select_charts]").find("option[value='"+cid+"']")
        conf_obj = options.data('conf')
        isappend = false
        if($("#chart_"+cid).length==0){
            isappend = true
        }else{
            if(confirm("已经存在此id，请确认是否继续添加？")){
                isappend = true
            }
        }
        if(isappend){
            html = new Array()
            html.push("<tr id='chart_"+conf_obj.id+"'>")
            html.push("<td>"+conf_obj.id+"</td>")
            html.push("<td><label>"+conf_obj.name+"</label><input type='text' class='form-control' style='display:none' value='"+conf_obj.id+"' name='ids'></td>")
            html.push("<td><button type='button' class='btn btn-defalut chart_up' title='move up'><span class='glyphicon glyphicon-arrow-up'></span></button><button type='button' class='btn btn-defalut chart_down' title='move down'><span class='glyphicon glyphicon-arrow-down'></span></button><button type='button' class='btn btn-defalut chart_del' title='delete'><span class='glyphicon glyphicon-remove'></span></button></td>")
            html.push("</tr>")
            $("#data_group").append(html.join(""))
            bind_on()
            get_customs_by_datasource(get_charts_ids(),customs_global,get_params())
        }
    })
    $("#add_chart_iframe").on("click",function(){
        input_name = $("input[name=input_name]").val()
        input_id = md5(input_name)
        input_iframe = $("input[name=input_iframe]").val()
        isappend = false
        if($("#chart_"+input_id).length==0){
            isappend = true
        }else{
            if(confirm("已经存在此id，请确认是否继续添加？")){
                isappend = true
            }
        }
        if(isappend){
            html = new Array()
            html.push("<tr id='chart_"+input_id+"'>")
            html.push("<td>"+input_id+"</td>")
            html.push("<td><label>"+input_name+"</label><input type='text' class='form-control' style='display:none' value=\""+input_name+":"+input_iframe.replace(/\"/g,"&quot;")+"\" name='ids'></td>")
            html.push("<td><button type='button' class='btn btn-defalut chart_up' title='move up'><span class='glyphicon glyphicon-arrow-up'></span></button><button type='button' class='btn btn-defalut chart_down' title='move down'><span class='glyphicon glyphicon-arrow-down'></span></button><button type='button' class='btn btn-defalut chart_del' title='delete'><span class='glyphicon glyphicon-remove'></span></button></td>")
            html.push("</tr>")
            $("#data_group").append(html.join(""))
            bind_on()
            get_customs_by_datasource(get_charts_ids(),customs_global,get_params())
        }
    })
    bind_on()
    $("select[name=params_types]").on("change",function(){
        if($(this).val()==0){
            $("#params_modal").find(".for_select").css("display","none")
        }else{
            $("#params_modal").find(".for_select").css("display","inline")
        }
    })
    $("#params_modal").find("button[class*=submit]").on("click",function(){
        obj = {}
        params_modal = $("#params_modal")
        obj['globals'] = {}
        obj['globals']['params_name'] = params_modal.find("input[name=params_name]").val()
        obj['globals']['params_types'] = params_modal.find("select[name=params_types]").val()
        obj['globals']['params_default'] = params_modal.find("input[name=params_default]").val()
        obj['globals']['params_counts'] = params_modal.find("input[name=params_counts]").val()
        obj['globals']['params_datasource'] = params_modal.find("textarea[name=params_datasource]").val()
        obj['globals']['params_customs_name'] = params_modal.find("input[name=params_customs_name]").val()
        params_types = "null"
        obj['params_types'] = obj['globals']['params_types']
        if(obj['params_types']==0){
            params_types = "input"
        }else if(obj['params_types']==1){
            params_types = "select"
        }else{
            params_types = "null"
        }
        obj['params_customs_name'] = obj['globals']['params_customs_name']
        tr_obj = $("#params_group").find("td:contains('"+obj['params_customs_name']+"')").parents("tr")
        tr_obj.find("input[name=search_params]").val(JSON.stringify(obj).replace(/\"/g,"&quot;"))
        tr_obj.find("input[name=search_params]").prev().text(params_types)
    })
})

function get_charts_ids(){
    ids=new Array()
    $("#data_group").find("input[name=ids]").each(function(){
        if(!isNaN($(this).val())){
            ids.push($(this).val())
        }
    })
    return ids
}

function get_params(){
    params = new Array()
    $("#params_group").find("input[name=search_params]").each(function(){
        params.push(JSON.parse($(this).val().replace(/&quot;/g,"\"")))
    })
    return params
}

function get_customs_by_datasource(ids,customs,params){
    customs_array = {}
    for(item in ids){
        for(it in customs[ids[item]]['customs']){
            customs_array[it]=true
        }
    }
    html = ""
    old = new Array()
    for(item in params){
        if(params[item].hasOwnProperty('globals')&&customs_array.hasOwnProperty(params[item]['params_customs_name'])){
            html += generate_html(params[item])
            old.push(params[item]['params_customs_name'])
        }
    }
    for(item in customs_array){
        if($.inArray(item,old)==-1){
            globals = {}
            globals['params_customs_name']=item
            globals['params_types']="-1"
            globals['globals']={}
            html += generate_html(globals)
        }
    }
    $("#params_group").children().remove()
    $("#params_group").append(html)
    bind_on()
}

function generate_html(rowobj){
    html = new Array()
    html.push('<tr>')
    html.push("<td>"+rowobj['params_customs_name']+"</td>")
    if(rowobj['params_types']==0){
        html.push('<td><label>input</label>')
    }else if(rowobj['params_types']==1){
        html.push('<td><label>select</label>')
    }else{
        html.push('<td><label>null</label>')
    }
    
    html.push('<input type="text" class="form-control" style="display:none" value="'+JSON.stringify(rowobj).replace(/\"/g,"&quot;")+'" name="search_params"></td>')
    html.push("<td><button type='button' class='btn btn-defalut chart_up' title='move up'><span class='glyphicon glyphicon-arrow-up'></span></button><button type='button' class='btn btn-defalut chart_down' title='move down'><span class='glyphicon glyphicon-arrow-down'></span></button><button type='button' class='btn btn-defalut params_edit' title='edit'><span class='glyphicon glyphicon-edit'></span></button><button type='button' class='btn btn-defalut params_del' title='delete'><span class='glyphicon glyphicon-remove'></span></button></td>")
    html.push("</tr>")
    return html.join("")
}

function init_modal(obj,params_customs_name){
    params_modal = $("#params_modal")
    params_modal.find("input[name=params_name]").val(get_key(obj,"params_name"))
    params_types = 0
    if(get_key(obj,"params_types",0)==""){
        params_types = 0
    }else{
        params_types = get_key(obj,"params_types",0)
    }
    params_modal.find("select[name=params_types]").select2('val',params_types)
    params_modal.find("input[name=params_default]").val(get_key(obj,"params_default"))
    params_modal.find("input[name=params_counts]").val(get_key(obj,"params_counts"))
    params_modal.find("textarea[name=params_datasource]").val(get_key(obj,"params_datasource"))
    params_modal.find("input[name=params_customs_name]").val(params_customs_name)
    if(get_key(obj,"params_types")==0){
        params_modal.find(".for_select").css("display","none")
    }else{
        params_modal.find(".for_select").css("display","inline")
    }
    params_modal.modal()
}
function get_key(obj,key){
    defaults = arguments[2] ? arguments[2] : "";
    if(obj&&obj.hasOwnProperty(key)){
        return obj[key]
    }else{
        return defaults
    }
}
function bind_on(){
    $("button[class*=chart_del]").on("click",function(){
        $(this).parents("tr").remove()
        var customs_global = {}
        $("select[name=select_charts]").find("option").each(function(){
            customs_global[$(this).val()]=$(this).data("conf")
        })
        get_customs_by_datasource(get_charts_ids(),customs_global,get_params())
    })
    $("button[class*=params_del]").on("click",function(){
        obj=$(this).parents("tr").find("input[name=search_params]")
        globals = {}
        globals['params_customs_name']=item
        globals['params_types']="null"
        globals['globals']={}
        obj.val(JSON.stringify(globals).replace(/\"/g,"&quot;"))
        obj.prev().text("null")
    })
    $("button[class*=chart_up]").on("click",function(){
        old=$(this).parents("tr")
        news = old.prev()
        if(news.length>0){
            news.before(old)
        }
    })
    $("button[class*=params_edit]").on("click",function(){
        confs=$(this).parents("tr").find("input[name=search_params]").val()
        confs=JSON.parse(confs.replace(/&quot;/g,"\""))
        init_modal(confs['globals'],confs['params_customs_name'])
    })
    $("button[class*=chart_down]").on("click",function(){
        old=$(this).parents("tr")
        news = old.next()
        if(news.length>0){
            news.after(old)
        }
    })
}