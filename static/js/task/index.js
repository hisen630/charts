$(function(){
    $("#search_btn").on("click",function() {
        $('#maingrid').bootgrid('reload');
    });
    $(".datepicker").datetimepicker({
        language:  'zh-CN',
        format:"yyyy-mm-dd hh:ii:ss",
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
    })
    $("#maingrid").bootgrid({
        navigation:0,
        rowCount:20,
        ajax: true,
        sorting: false,
        url: "/task/search",
        identifier: "id",
        statusMapping: {
            0: "danger",
            1: "",
            2: "success"
        },
        requestHandler: function(request) {
            return $("#mainform").serialize() + "&" + $.param(request);
        },
        formatters: {
            "types": function(column, row){
                if(row.types==0){
                    return "mysql"
                }else if(row.types==1){
                    return "计算型mysql"
                }else if(row.types==2){
                    return "fakecube"
                }else if(row.types==3){
                    return "hive"
                }else {
                    return "未知"
                }
            },
            "commands": function(column, row){
                return "<a type=\"button\" class=\"btn btn-xs btn-default\" title=\"edit datasource\" data-row-id=\"" + row.id + "\" target=\"_blank\" href=\"/task/edit?id="+row.id+"\"><span class=\"glyphicon glyphicon-pencil\"></span></a> "+
                "<a type=\"button\" class=\"btn btn-xs btn-default\" title=\"view log\" data-row-id=\"" + row.id + "\" target=\"_blank\" href=\"/task/run_index?tid="+row.id+"\"><span class=\"glyphicon glyphicon-book\"></span></a> "+
                "<button type=\"button\" class=\"btn btn-xs btn-default command_run_once\" title=\"run once\" data-row_id=\"" + row.id + "\" ><span class=\"glyphicon glyphicon-play\"></span></button> ";
            },
        },
        templates: {
        }
    }).on("loaded.rs.jquery.bootgrid",function(e){
        $("button[class*=command_run_once]").on("click",function(){
            $('#myModal').modal("hide")
            $('#myModal').find("input[name=custom_time]").val("")
            $('#myModal').find("input[name=id]").val($(this).data("row_id"))
            $('#myModal').modal("show")
        })
    })
    $("#myModal").find(".submit").on("click",function(){
        id = $('#myModal').find("input[name=id]").val()
        custom_time = $('#myModal').find("input[name=custom_time]").val()
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/task/run_single',
            timeout:20000,
            dataType:"json",
            data:{"tid":id,"custom_time":custom_time,"opertype":2},// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    alert(data.msg)
                }else{
                    alert(data.msg)
                }
            }
        });
    })
})
