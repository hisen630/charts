function write_view_struct(data){
    $("#data_show").children().remove()
    for(item in table_title){
        html = new Array()
        html.push('<table class="table table-condensed table-hover table-striped">')
        html.push('<thead><tr><th>')
        html.push(table_title[item])
        html.push('</th></tr></thead><tbody>')
        for(it in data[table_title[item]]){
            html.push("<tr><td>"+data[table_title[item]][it]+"</td></tr>")
        }
        html.push('</tbody></table>')
        $("#data_show").append(html.join(""))
    }
}
$(function(){
    table_title = new Array("dimensions_in_select","metrics","grouping_sets","tables")
    $(".datepicker").datetimepicker({
        language:  'zh-CN',
        format:"yyyy-mm-dd hh:ii:ss",
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
    })

    //保存内容
    $("#submit").on("click",function(){
        $("#sql_editor").text(sql_editor.getValue());
        params = $(".form-horizontal").serialize();
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/task/save',
            timeout:20000,
            dataType:"json",
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    alert(data.msg)
                    window.location.href = "/task/edit?id="+data.data
                }else{
                    alert(data.msg)
                }
            }
        });
    });
    view_struct = $("#data_show").data('conf')
    if(view_struct){
        write_view_struct(view_struct)
    }

    $("#view_result").click(function(){
        $("#sql_editor").text(sql_editor.getValue());
        params = $(".form-horizontal").serialize();
        $.ajax({
            type: "POST",
            url:'/task/get_data',
            timeout:20000,
            dataType:"json",
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    write_view_struct(data.data)
                }else{
                    alert(data.msg)
                }
            }
        });
    })
    $("#sql_show").on("click",function(){
        $('#myModal').modal("hide")
        $("#sql_content").text('')
        $("#sql_editor").text(sql_editor.getValue());
        params = $(".form-horizontal").serialize();
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/task/get_sql',
            timeout:20000,
            dataType:"json",
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    $("#sql_content").text(data.data)
                    $('#myModal').modal("show")
                }else{
                    alert(data.msg)
                }
            }
        });
    })
})
var sql_editor = CodeMirror.fromTextArea(document.getElementById("sql_editor"), {
    mode: {
        name: "text/x-mysql"
    },
    indentWithTabs: true,
    smartIndent: true,
    lineNumbers: true,
    indentUnit: 4,
    matchBrackets : true,
    autofocus: true,
    theme: "material",
    hintOptions: {
        tables: {
          users: {name: null, score: null, birthDate: null},
          countries: {name: null, population: null, size: null}
        }
    }
});
