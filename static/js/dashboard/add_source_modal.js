function mysql_modal(types,conf){
    customs = arguments[2] ? arguments[2] : ''
    $("#mysql").find("input[name=name]").val(conf.name)
    $("#mysql").find("input[name=old_customs]").val(JSON.parse(conf.conf).customs)
    $("#mysql").find("input[name=customs]").val(customs)
    $("#mysql").find("input[name=conf]").val(escape(JSON.stringify(conf)))
    $("#mysql").find("input[name=conf]").data('types',conf.types)
    $("#mysql").modal()
}

function escape(str){
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;")
}

function unescape(str){
    return $("<div>").html(str).text()
}

function mysql_modal_save(obj){
    name = $("#mysql").find("input[name=name]").val()
    conf = $("#mysql").find("input[name=conf]").val()
    customs = $("#mysql").find("input[name=customs]").val()
    write_datasource_html(name,customs,conf)
}

function mysql_caculate_modal(types,conf){
    customs = arguments[2] ? arguments[2] : ''
    $("#mysql").find("input[name=name]").val(conf.name)
    $("#mysql").find("input[name=old_customs]").val(JSON.parse(conf.conf).customs)
    $("#mysql").find("input[name=customs]").val(customs)
    $("#mysql").find("input[name=conf]").val(escape(JSON.stringify(conf)))
    $("#mysql").find("input[name=conf]").data('types',conf.types)
    $("#mysql").modal()
}

function mysql_caculate_modal_save(obj){
    name = $("#mysql").find("input[name=name]").val()
    conf = $("#mysql").find("input[name=conf]").val()
    customs = $("#mysql").find("input[name=customs]").val()
    write_datasource_html(name,customs,conf)
}
