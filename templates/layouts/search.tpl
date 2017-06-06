{% extends "layouts/nav.tpl" %}
{% block dot_js %}
{{ super() }}
    <script src="/static/plugin/doT.min.js" type="text/javascript"></script>
    <script id="customSelect_tpl" type="text/x-dot-template">
        {/? it[prop].option/}
            <div class="col-md-{/=it[prop].rowNum || 2/}">
                <select data-limit="{/=it[prop].dataLimit || 100/}" name="{/=it[prop].name || ''/}{/? it[prop].multiple/}[]{/?/}" class="form-control {/=it[prop].class || ''/}" placeholder="{/=it[prop].placeholder || ''/}" {/=it[prop].multiple||''/} {/=it[prop].custom || ''/}>
                        {/for(var optionAry in it[prop].option) { /}
                            <option value="{/=it[prop].option[optionAry].value/}" {/? $.inArray(it[prop].option[optionAry].value,it[prop].selected) >-1 /}selected="selected"{/?/}>{/=it[prop].option[optionAry].content /}</option>
                        {/ } /}
                </select>
            </div>
        {/?/}
    </script>

    <script id="customInput_tpl" type="text/x-dot-template">
        <div class="col-md-{/=it[prop].rowNum || 2/}">
            <input type="{/=it[prop].type || 'text'/}" value="{/=it[prop].value/}" placeholder="{/=it[prop].placeholder || ''/}" name="{/=it[prop].name || ''/}" class="form-control {/=it[prop].class || ''/}" style="{/=it[prop].style || ''/}" valid='{/=it[prop].valid || ''/}' {/=it[prop].custom || ''/}>
        </div>
    </script>

    <script id="customTextarea_tpl" type="text/x-dot-template">
        <div class="col-md-{/=it[prop].rowNum || 2/}">
            <textarea cols="{/=it[prop].cols || 20/}" name="{/=it[prop].name || ''/}" class="form-control {/=it[prop].class || ''/}" placeholder="{/=it[prop].placeholder || ''/}" style="{/=it[prop].style || ''/}" valid='{/=it[prop].valid || ''/}' {/=it[prop].custom || ''/}>{/=it[prop].value/}
            </textarea>
        </div>
    </script>

    <script id="customButton_tpl" type="text/x-dot-template">
        <div class="col-md-{/=it[prop].rowNum || 2/}">
            <button type="{/=it[prop].type||'button'/}" value="{/=it[prop].value || ''/}" name="{/=it[prop].name || ''/}" class="btn btn-outline {/=it[prop].class || 'btn-default'/}" {/=it[prop].custom||''/}>{/=it[prop].content||'error'/}</button>
        </div>
    </script>

    <script id="customLabel_tpl" type="text/x-dot-template">
         <label class="col-md-{/=it[prop].rowNum || 1/} control-label {/=it[prop].class || ''/}" style="{/=it[prop].style || ''/}" {/=it[prop].custom || ''/} >{/=it[prop].content||''/}</label>
    </script>
    <script id="customGroup_tpl" type="text/x-dot-template">
        <div class="form-group">
            {/ for(var prop in it) { /}
                {/var tmpTplType=it[prop].dtype;/}
                {/? tmpTplType=='label'/}
                    {/#def.label || "error"/}
                {/?? tmpTplType=='input'/}
                    {/#def.input || "error"/}
                {/?? tmpTplType=='select'/}
                    {/#def.select || "error"/}
                {/?? tmpTplType=='category'/}
                    {/#def.category || "error"/}
                {/?? tmpTplType=='button'/}
                    {/#def.button || "error"/}
                {/?? tmpTplType=='textarea'/}
                    {/#def.textarea || "error"/}
                {/?/}
            {/ } /}
        </div>
    </script>
{% endblock %}
{% block search %}
<div class="col-lg-12">
    <div id="well" class="well searchColor">
        <lable id="search_conf" data-conf='{{searchForMat}}' style="display:none"></lable>
        <form class="form-horizontal" role="form" onsubmit="return validSearchTpl('Searchform')" id="Searchform">
        </form>
    </div>
</div>
{% endblock %}
{% block footer %}
    {{ super() }}
<script type="text/javascript">
    var def = {
        label: $('#customLabel_tpl').text(),
        input: $('#customInput_tpl').text(),
        select: $('#customSelect_tpl').text(),
        category: $('#customCategory_tpl').text(),
        button: $('#customButton_tpl').text(),
        textarea: $('#customTextarea_tpl').text()
    };
    var data = $("#search_conf").data("conf")
    var setting = {
      evaluate:    /\{\/([\s\S]+?)\/\}/g,
      interpolate: /\{\/=([\s\S]+?)\/\}/g,
      encode:      /\{\/!([\s\S]+?)\/\}/g,
      use:         /\{\/#([\s\S]+?)\/\}/g,
      define:      /\{\/##\s*([\w\.$]+)\s*(\:|=)([\s\S]+?)#\/\}/g,
      conditional: /\{\/\?(\?)?\s*([\s\S]*?)\s*\/\}/g,
      iterate:     /\{\/~\s*(?:\}\}|([\s\S]+?)\s*\:\s*([\w$]+)\s*(?:\:\s*([\w$]+))?\s*\/\})/g,
      varname: 'it',
      strip: true,
      append: true,
      selfcontained: false
    }
    for (i in data){
        var pagefn = doT.template($('#customGroup_tpl').text(),setting,def);
        $('#Searchform').append(pagefn(data[i]));
    }
    $(".select2-single").each(function(){
        $(this).select2({
            language: "zh-CN",
            placeholder:$(this).attr("placeholder")
        });
    });
    $(".select2-multiple").each(function(){
        $(this).select2({
            language: "zh-CN",
            maximumSelectionSize: $(this).attr("data-limit"),
            placeholder:$(this).attr("placeholder")
        });
    });
</script>
{% endblock %}