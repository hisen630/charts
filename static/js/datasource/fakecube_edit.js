function change_select(obj){
    tid = obj.val()
    tables = obj.find("option[value="+tid+"]").data("tables")
    $("select[name=tid_table]").children().remove()
    html = new Array()
    for(it in tables){
        html.push("<option value='"+tables[it]['id']+"'>"+tables[it]['table_tag']+"</option>")
    }
    $("select[name=tid_table]").append(html.join(""))
    $("select[name=tid_table][class*=multiple]").select2({
        minimumResultsForSearch:1
    })
}

$(function(){
    $(".multiple").select2({
        minimumResultsForSearch:1
    })
    $("select[name=tid]").on("change",function(){
        change_select($(this))
    })
    change_select($("select[name=tid]"))
    //保存内容
    $("#submit").on("click",function(){
        $("#sql_editor").text(sql_editor.getValue());
        $("#python_editor").text(python_editor.getValue());
        params = $(".form-horizontal").serialize();
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/datasource/save',
            timeout:20000,
            dataType:"json",
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    alert(data.msg)
                    window.location.href = "/datasource/edit?id="+data.data
                }else{
                    alert(data.msg)
                }
            }
        });
    });
    $("#create_notebook").click(function(){
        $("#sql_editor").text(sql_editor.getValue());
        $("#python_editor").text(python_editor.getValue());
        params = $(".form-horizontal").serialize();
        $.ajax({
            type: "POST",
            url:'/notebook/new',
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
    })
    $("#view_result").click(function(){
        $("#sql_editor").text(sql_editor.getValue());
        $("#python_editor").text(python_editor.getValue());
        params = $(".form-horizontal").serialize();
        $.ajax({
            type: "POST",
            url:'/datasource/get_data',
            timeout:20000,
            dataType:"json",
            data:params,// 你的formid
            error: function(request) {
                alert("网络请求失败，请检查网络")
            },
            success: function(data) {
                if(data.status){
                    $("#data_show").children().remove()
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
        $("#python_editor").text(python_editor.getValue());
        params = $(".form-horizontal").serialize();
        // 异步加载数据
        $.ajax({
            type: "POST",
            url:'/datasource/get_sql',
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