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
    $("#add_chart").on("click",function(){
        cid = $("select[name=select_charts]").val()
        options = $("select[name=select_charts]").find("option[value='"+cid+"']")
        conf_obj = options.data('conf')
        isappend = false
        if($("#datasource_"+cid).length==0){
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
        }
    })
    bind_on()
})

function bind_on(){
    $("button[class*=chart_del]").on("click",function(){
        $(this).parents("tr").remove()
    })
    $("button[class*=chart_up]").on("click",function(){
        old=$(this).parents("tr")
        news = old.prev()
        if(news.length>0){
            news.before(old)
        }
    })
    $("button[class*=chart_down]").on("click",function(){
        old=$(this).parents("tr")
        news = old.next()
        if(news.length>0){
            news.after(old)
        }
    })
}