$(function(){
	$("#search_btn").click(function() {
        $('#maingrid').bootgrid('reload');
    });
	$("#maingrid").bootgrid({
        navigation:0,
        rowCount:20,
        ajax: true,
        sorting: false,
        url: "/dashboard/search",
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
        	"commands": function(column, row){
	            return "<a type=\"button\" class=\"btn btn-xs btn-default command-edit\" data-row-id=\"" + row.id + "\" target=\"_blank\" href=\"/dashboard/edit?id="+row.id+"\"><span class=\"glyphicon glyphicon-pencil\"></span></a> " +
                "<a type=\"button\" class=\"btn btn-xs btn-default command-edit\" data-row-id=\"" + row.id + "\" target=\"_blank\" href=\"/dashboard/get_chart?id="+row.id+"\"><span class=\"glyphicon glyphicon-search\"></span></a> ";
	        },
        },
        templates: {
        }
    })
})