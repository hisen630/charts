$(function(){
    $("#search_btn").click(function() {
        $('#maingrid').bootgrid('reload');
    });
    $("#maingrid").bootgrid({
        navigation:0,
        rowCount:20,
        ajax: true,
        sorting: false,
        url: "/datasource/search",
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
                return "<a type=\"button\" class=\"btn btn-xs btn-default command-edit\" data-row-id=\"" + row.id + "\" target=\"_blank\" href=\"/datasource/edit?id="+row.id+"\"><span class=\"glyphicon glyphicon-pencil\"></span></a> ";
            },
        },
        templates: {
        }
    })
})
