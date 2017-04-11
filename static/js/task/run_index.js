$(function(){
    $("#search_btn").click(function() {
        $('#maingrid').bootgrid('reload');
    });
    $("#maingrid").bootgrid({
        navigation:2,
        rowCount:10,
        ajax: true,
        sorting: false,
        url: "/task/run_search",
        identifier: "id",
        statusMapping: {
            0: "",
            1: "danger",
            2: "success",
            3: "info",
        },
        requestHandler: function(request) {
            return $("#mainform").serialize() + "&" + $.param(request);
        },
        formatters: {
            "status": function(column, row){
                if(row.status==0){
                    return "初始化"
                }else if(row.status==1){
                    return "失败"
                }else if(row.status==2){
                    return "成功"
                }else if(row.status==3){
                    return "取消"
                }
            },
            "types": function(column, row){
                if(row.types==0){
                    return "未知"
                }else if(row.types==1){
                    return "自动"
                }else if(row.types==2){
                    return "手动"
                }
            },
            "commands": function(column, row){
                cancel = ""
                if(row.status == 0){
                    cancel = "<a type=\"button\" title=\"retry\" class=\"btn btn-xs btn-default command_cancel\" data-row_id=\""+row.id+"\" data-row_time=\""+row.run_time+"\" data-row_name=\""+row.name+"\" data-row-id=\"" + row.id + "\"><span class=\"glyphicon glyphicon-remove\"></span></a> "
                }
                retry = "<a type=\"button\" title=\"retry\" class=\"btn btn-xs btn-default command_retry\" data-row_id=\""+row.id+"\" data-row_time=\""+row.run_time+"\" data-row_name=\""+row.name+"\" data-row-id=\"" + row.id + "\"><span class=\"glyphicon glyphicon-repeat\"></span></a> "
                
                return retry+cancel;
            },
        },
        templates: {
        }
    }).on("loaded.rs.jquery.bootgrid",function(e){
        $(".command_retry").on("click",function(){
            if(confirm("请确认是否重试此任务？任务名称："+$(this).data("row_name")+";任务时间"+$(this).data("row_time"))){
                // 异步加载数据
                $.ajax({
                    type: "POST",
                    url:'/task/run_single',
                    timeout:20000,
                    dataType:"json",
                    data:{"lid":$(this).data("row_id"),"opertype":2},// 你的formid
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
            }
        })
        $(".command_cancel").on("click",function(){
            if(confirm("请确认是否取消此任务？任务名称："+$(this).data("row_name")+";任务时间"+$(this).data("row_time"))){
                // 异步加载数据
                $.ajax({
                    type: "POST",
                    url:'/task/run_cancel',
                    timeout:20000,
                    dataType:"json",
                    data:{"lid":$(this).data("row_id")},// 你的formid
                    error: function(request) {
                        alert("网络请求失败，请检查网络")
                    },
                    success: function(data) {
                        alert(data.msg)
                    }
                });
            }
        })
    })
})
