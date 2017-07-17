{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
    <link rel="stylesheet" href="/static/plugin/highchart_edit/highcharts-editor.min.css">
    <link rel="stylesheet" href="/static/plugin/bootstrap-table/bootstrap-table.min.css">
{% endblock %}
{% block content %}
    <style type="text/css">
        body {
            width: 100%;
        }

        fieldset {
            padding: .35em 2em 1em 2em;
            margin: 0 2px;
            border: 1px solid silver
        }

        legend {
            padding: .5em;
            border: 0;
            width: auto
        }

        .popover {
            max-width: 1000px;
            min-width: 300px;
        }

        .draglist {
            padding: 4px 5px;
            margin-bottom: 5px;
            border: 1px dashed #ccc;
            cursor: move;
            font-size: 12px
        }

        .draglist:hover {
            border-color: #cad5eb;
            background-color: #eee;
        }

        .fliterzone form {
            border-top: 1px solid #ccc;
            padding: 1% 0 1% 0;
        }

        .marked {
            text-align: center;
            padding: 0 4px 0 10px;
            margin: 4px;
            float: left;

        }

        .endbox {
            margin: 10px 0;
            padding: 0 5px;
            border: 1px solid #ccc;
            overflow: hidden;
            height: 34px;
        }


    </style>

    <div class="row">
        <div class="col-sm-3">
            <label for="c01-select">表</label><input name="db" id="c01-select" class="form-control"/>
            <label for="c02-select">库</label><input name="table" id="c02-select" class="form-control"/>
            <label>搜索</label>
            <input id="query" name="query" class='form-control text-center' type='text'
                   placeholder='Query(*)'/>
            <fieldset>
                <legend>维度</legend>
                <div id="dimension" class="row"></div>
            </fieldset>
            <fieldset>
                <legend>指标</legend>
                <div id="index" class='row'></div>
            </fieldset>
            {#            <div style="height: 10000px;"></div>#}
        </div>

        <div class="col-sm-9 col-sm-offset-3" style="position: absolute;">
            <div style="position: fixed;width: 50%;">
                <div class="row">
                    <fieldset class="fliterzone">
                        <legend>过滤</legend>
                        <div class="content"></div>
                    </fieldset>

                    <div class='columnszone endbox text-center'>Columns</div>
                    <div class='rowszone endbox text-center'>Rows</div>
                </div>

                <div class="col-sm-6">
                    <div class="col-sm-6 checkbox" style="margin-top: 5px">
                        <label><input id="form-btn" type="checkbox" name="form">表格</label>
                    </div>
                    <div class="col-sm-6 pull-right">
                        <button id="setting" class="btn btn-sm btn-success btn-block">编辑图表</button>
                    </div>
                </div>
                <div class="col-sm-6">
                    <button id="preview" class="btn btn-sm btn-block">预览</button>
                </div>
                <div id="show-content" class="row" style="padding-top:20px;">
                    <div class="row">
                        <div id="chart-show" style="min-height:400px;"></div>
                    </div>
                    <div class="table-responsive hidden">
                        <table id="table-show" class="table table-hover table-striped"
                               data-search="true"
                               data-show-export="true"
                               data-show-toggle="true"
                        ></table>
                    </div>
                </div>
            </div>
        </div>

    </div>
    {#    hidden#}
    <div class="aggs-box hidden">

        {#    拖动后的对象   draggable="true" tabindex="0" role="button" data-toggle="popover"  #}
        <div class='marked btn btn-sm btn-primary' draggable="true">
            拖动后的对象
            <span class="glyphicon glyphicon-chevron-up" style="color: black;margin-left: 5px"></span>
        </div>
        {#    维度指标对象  #}
        <div class="draglist text-center" draggable="true">维度指标标题</div>
        {#        过滤框内的日期对象 #}
        <form class="date-box form-inline form-group-sm" onsubmit="return false;">
            <div class="form-group">
                <label>标题</label>
                <input name="min" type="datetime" class="form-control" placeholder="开始时间">
            </div>
            <div class="form-group">
                <input name="max" type="datetime" class="form-control " placeholder="结束时间">
            </div>
            <button type="button" class="btn btn-danger btn-xs">
                <span class="glyphicon glyphicon-remove"></span>
            </button>
        </form>
        {# 过滤的数字对象  #}
        <form class="number-box form-inline form-group-sm" onsubmit="return false;">
            <div class="form-group">
                <label>标题</label>
                <select name="oper" class="form-control" style="width: 160px"></select>
            </div>
            <div class="form-group">
                <input name="value" type="text" class="form-control" placeholder="输入过滤内容">
            </div>
            <button class="btn btn-danger btn-xs"><span class="glyphicon glyphicon-remove"></span>
            </button>
        </form>
        {#      指标的数字对象  #}
        <form class="index-number">
            <label class="col-sm-4">聚合方法</label>
            <label class="col-sm-8">
                <input name="agg" type="text" class="form-control input-sm">
            </label>
        </form>

        {# 维度字符样式 #}
        <form class="dimension-string">
            <div class="form-group form-group-sm">
                <label class="col-sm-3">排序</label>
                <label class="col-sm-9">
                    <select name="order" class="form-control input-sm">
                        <option value="desc">倒序</option>
                        <option value="asc">正序</option>
                    </select>
                </label>
            </div>
            <div class="form-group form-group-sm">
                <label class="col-sm-3">TOP</label>
                <label class="col-sm-9">
                    <input name="size" value="5" type="text" class="form-control input-sm" placeholder="默认为5">
                </label>
            </div>
        </form>
        {#    维度数值指定区间    #}
        <form class="dimension-number" onsubmit="return false;">
            <div class="form-inline">
                <div class="form-group form-group-sm">
                    <label></label>
                    <input name="start" type="text" class="form-control input-sm" placeholder="开始范围(0)">
                </div>
                <div class="form-group form-group-sm">
                    <label></label>
                    <input name="end" type="text" class="form-control input-sm" placeholder="结束范围">
                </div>
                <input type="hidden" name="oper" value="histogram">
                <button class="btn btn-xs btn-danger"><span class="glyphicon glyphicon-remove"></span></button>
            </div>
            <button class="btn btn-xs btn-block">添加</button>
        </form>
        {# 维度数字类型间隔类型 #}
        <form class="interval-number" onsubmit="return false;">
            <div class="form-inline">
                <div class="form-group form-group-sm">
                    <label></label>
                    <input name="interval" type="text" class="form-control input-sm" placeholder="间隔数字">
                </div>
                <input type="hidden" name="oper" value="histogram">
            </div>
        </form>
        {#  维度日期间隔类型  #}
        <form class="interval-date" onsubmit="return false;">
            <div class="form-inline">
                <div class="form-group form-group-sm">
                    <input name="interval" type="text" class="form-control input-sm" placeholder="间隔">
                    <select name="unit" class="form-control input-sm">
                        <option value="y">年</option>
                        <option value="M">月</option>
                        <option value="w">周</option>
                        <option value="d">日</option>
                        <option value="h">时</option>
                        <option value="m">分</option>
                        <option value="s">秒</option>
                    </select>
                </div>

                <input type="hidden" name="oper" value="histogram">
            </div>
        </form>
    </div>

{% endblock %}
{% block footer %}
    {{ super() }}
    <script> // 扩展
    String.prototype.trim = function () {
        return this.replace(/(^\s*)|(\s*$)/g, "");
    };
    //删除左边的空格
    String.prototype.ltrim = function () {
        return this.replace(/(^\s*)/g, "");
    };
    //删除右边的空格
    String.prototype.rtrim = function () {
        return this.replace(/(\s*$)/g, "");
    };
    Array.prototype.indexOf = function (val) {
        for (var i = 0; i < this.length; i++) {
            if (this[i] == val) return i;
        }
        return -1;
    };
    Array.prototype.remove = function (val) {
        var index = this.indexOf(val);
        if (index > -1) {
            this.splice(index, 1);
        }
    };
    Array.prototype.unique = function () {
        var res = [];
        var json = {};
        for (var i = 0; i < this.length; i++) {
            if (!json[this[i]]) {
                res.push(this[i]);
                json[this[i]] = 1;
            }
        }
        return res;
    };
    Array.prototype.clear = function () {
        this.splice(0, this.length);
        return this
    };
    function cloneObject(obj) {
        var str, newobj = obj.constructor === Array ? [] : {};
        if (typeof obj !== 'object') {
            return;
        } else if (window.JSON) {
            str = JSON.stringify(obj); //系列化对象
            newobj = JSON.parse(str); //还原
        } else {
            for (var i in obj) {
                newobj[i] = typeof obj[i] === 'object' ? cloneObject(obj[i]) : obj[i];
            }
        }
        return newobj;
    }


    function getOneByArray(array, key, value) { // 获得数组嵌套对象的中的一个对象
        for (var i = 0; i < array.length; i++) {
            if (array[i][key] == value) {
                return array[i]
            }
        }
    }
    function updateObject(old_object, new_object) {
        // 如果 val 被忽略
        for (var item in new_object) {
            if (typeof new_object[item] === "undefined") {
                // 删除属性
                delete old_object[item];
            }
            else {
                // 添加 或 修改
                old_object[item] = new_object[item];
            }
        }
        return old_object
    }
    function clearObject(object) {
        for (var item in object) {
            delete object[item];
        }
        return object
    }
    function checkJsonParams(object) {
        for (var item in object) {
            if (!object[item]) {
                return false
            }
        }
        return true
    }
    function clearDragover(JqObject) {
        JqObject.ondragover = function (event) {
            event.preventDefault();
            return true;
        };
        return JqObject
    }
    (function ($) { // Jquery转JSON
        $.fn.serializeJson = function () {
            var serializeObj = {};
            $(this.serializeArray()).each(function () {
                serializeObj[this.name] = this.value;
            });
            return serializeObj;
        };
    })(jQuery);


    log = console.log;
    function dir(object) {
        for (var item in object)
            console.log(item)
    }

    </script>
    <script src="/static/plugin/bootstrap-table/bootstrap-table.min.js"></script>
    <script src="/static/plugin/bootstrap-table/bootstrap-table-export.min.js"></script>
    <script src="/static/plugin/bootstrap-table/bootstrap-table-locale-all.min.js"></script>
    <script src="/static/plugin/bootstrap-table/tableExport.min.js"></script>
    <script src="/static/plugin/bootstrap-table/libs/FileSaver/FileSaver.min.js"></script>
    <script src="https://code.highcharts.com/stock/highstock.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/adapters/standalone-framework.js" type="text/javascript"
            charset="utf-8"></script>
    <script src="https://code.highcharts.com/highcharts-more.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/highcharts-3d.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/modules/data.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/funnel.js"></script>
    <script src="https://code.highcharts.com/modules/solid-gauge.js"></script>
    <script src="/static/plugin/highchart_edit/highcharts-editor.min.js"></script>
    <script src="/static/plugin/highchart_edit/highcharts-editor.advanced.min.js"></script>
    <script src="/static/plugin/highchart_edit/highcharts.editor.lang.zh_cn.js"></script>
    <script src="/static/plugin/highchart_edit/highed.meta.charts.js"></script>
    <script src="/static/plugin/highchart_edit/highed.dataimporter.js"></script>
    <script>
        var dbs = {{ dbs | tojson | safe }}, mappings = {{ mappings | tojson | safe }};
    </script>
    <script type="text/javascript">
        // 标记数据  ===========================================================================================================
        var hit_drag = {}, request_params = {}, settings = {}, aggsBox = $(".aggs-box");
        // 当前被拖动的对象 / 请求参数的请求体 / chart的配置代码  / 复制全部节点
        // 重置功能 ============================================================================================================
        var index = $('#index'), dimension = $('#dimension'), columns = $(".columnszone"), rows = $(".rowszone");

        function indexDimensionReset(dom1, dom2) { // 重置 维度和指标
            index.empty();
            dimension.empty();
            index.append(dom1);
            dimension.append(dom2);

        }
        function filterReset(html) { // 重置过滤
            $(".fliterzone .content").html(html ? html : "")
        }
        function columnRowReset() { // 重置准备提交的内容
            columns.html('Columns');
            rows.html('Rows')
        }
        // 库表选择 ============================================================================================================
        var hit_tables = [], hit_db, hit_table, selected_db = $("#c01-select"),
            selected_table = $("#c02-select"); // 选中的库对应的表, 当前选中的数据库
        selected_db.select2({
            data: function () {
                var dbArr = [], i = 0;
                for (var item in dbs) {
                    dbArr.push({id: i, 'text': item});
                    i += 1
                }
                return dbArr
            }(),
            placeholder: '选择库',
            allowClear: true
        });


        selected_db.on("select2-selecting", function (e) {
            hit_db = (e.object || {}).text || Object.keys(dbs)[0];
            hit_tables.splice(0, hit_tables.length); //  清空数组内容

            var j = 0;
            for (var item in dbs[hit_db]) {
                hit_tables.push({id: j, 'text': item});
                j += 1
            }
            selected_table.select2('val', '0'); // 默认第一项
            selected_table.trigger("select2-selecting"); // 表选中第一个
        });
        selected_table.select2({
            data: hit_tables,
            placeholder: '请先选择库',
            allowClear: true
        });

        var dragList = aggsBox.find(".draglist:eq(0)");
        selected_table.on("select2-selecting", function (e) { // 每次选择表后 刷新左侧所有维度指标
            hit_table = dbs[hit_db][((e.object || {}).text || getOneByArray(hit_tables, "id", 0)["text"])];
            var dragZone = {"index": [], "dimension": []};
            for (var item in dragZone) {
                hit_table[item].forEach(function (temp) {
                    dragZone[item].push(dragList.clone(true).text(temp.label).data("info", updateObject(temp, {"class": item})));
                });
            }
            hit_drag.id = hit_table.id;
            indexDimensionReset(dragZone.index || [], dragZone.dimension || []);
            filterReset();
            columnRowReset();
            install_drags();

        });
        //  安装拖拉事件 ========================================================================================================

        function install_drags() { //
            // 添加操作
            $(".draglist").each(function () {
                this.ondragstart = function (ev) {
                    updateObject(hit_drag, ($(this).data("info"))); //  更新命中者信息
                    ev.dataTransfer.setDragImage(ev.target, 0, 0);
                    return true;
                };

            });
        }

        // 过滤区域映射 =========================================================================================================

        var hit_oper = [];
        aggsBox.find(".number-box button.btn-danger:last,.date-box button.btn-danger:last").each(function () { // 安装过滤框的关闭按钮事件
            $(this).click(function () {
                $(this).parent("form").remove()
            })
        });
        var commonFilterType = function () {
            var numberBox = aggsBox.find(".number-box").clone(true);
            numberBox.find("label:eq(0)").text(hit_drag.label); //  更改标题
            numberBox.data("info", cloneObject(hit_drag));
            var select = numberBox.find("select");
            for (var i = 0; i < hit_oper.length; i++) {
                select.append($("<option value='" + hit_oper[i] + "'>" + hit_oper[i] + "</option>"));
            }
            return numberBox
        };
        var typesMapping = { // 类型映射
            "number": commonFilterType,
            "string": commonFilterType,
            "date": function () {
                var dateBox = aggsBox.find(".date-box").clone(true);
                dateBox.find("label:eq(0)").text(hit_drag.label); //  更改标题
                dateBox.data("info", cloneObject(hit_drag));
                return dateBox
            }
        };

        // 过滤区域安装拖动对象放下事件 ===========================================================================================
        clearDragover($(".fliterzone:eq(0)")[0]).ondrop = function (ev) {
            log(updateObject(hit_oper.clear(), ((mappings[hit_drag.source_type] || {})[hit_drag.type] || {}).filter));// 更新对象
            $('.fliterzone .content').append(typesMapping[hit_drag.type]);
            return false;
        };

        // 标签被拖动后绑定所有的事件产生的标签 ====================================================================================
        var popoverHide = function (e) {
            $(this).find("span:eq(0)").attr("class", "glyphicon glyphicon-chevron-up");
            var info = updateObject($(this).data("info"), $(this).next().find("form").serializeJson());
            $(this).data("info", info);
        };
        var PopoverContentMapping = {
            dimension: {
                "number": {
                    "html": aggsBox.find(".interval-number:eq(0)"),
                    "hide": popoverHide
                },
                "string": {
                    "html": aggsBox.find(".dimension-string:eq(0)"),
                    "hide": popoverHide
                },
                "date": {
                    "html": aggsBox.find(".interval-date:eq(0)"),
                    "hide": popoverHide
                }
            },
            index: {
                "number": {
                    "html": aggsBox.find(".index-number:eq(0)"),
                    "show": function (e) {
                        var hit_aggregates = ((mappings[hit_drag.source_type] || {})[hit_drag.type] || {}).aggregates || [];
                        if (!this.selectInit) { // 初始化
                            var popover = $(this).next();
                            popover.find("input:eq(0)").select2({
                                data: function () {
                                    var temp = [];
                                    for (var i = 0; i < hit_aggregates.length; i++) {
                                        temp.push({id: hit_aggregates[i], 'text': hit_aggregates[i]})
                                    }
                                    return temp
                                }(),
                                placeholder: '选择聚合函数',
                                allowClear: true
                            }).select2("val", "求和"); // 默认求和;
                            this.selectInit = true
                        }


                    },
                    "hide": popoverHide
                }
            }

        };
        function bindPopover(tag) { // 初始化popover框 输入一个JQuery对象
            var hit = PopoverContentMapping[hit_drag.class][hit_drag.type], html = hit.html.clone(true);
            tag.popover({
                html: true,
                trigger: "manual",
                placement: "bottom",
                title: hit_drag.field + " (" + hit_drag.label + ")",
                content: html
            }).click(function (event) {
                $('.popover').not($(this)).popover("hide"); // 同时只能打开一个popover
                $(this).popover("toggle"); // 切换状态
                event.stopPropagation();
            }).on("shown.bs.popover", hit.show).on("hide.bs.popover", hit.hide).on("shown.bs.popover", function () {
                $(this).find("span:eq(0)").attr("class", "glyphicon glyphicon-chevron-down");
            });
            tag.data("info", updateObject((tag.data("info") || {}), html.serializeJson())); // 绑定数据
            return tag
        }
        function bingTag(tag) {
            tag.data("info", updateObject((tag.data("info") || {}), cloneObject(hit_drag))); // 绑定数据
            var span = tag.children("span:eq(0)").clone(true); // 事件一并克隆
            tag.text(hit_drag.label); // 更新文案
            tag.append(span); // 重新插入删除按钮
            return bindPopover(tag);
        }

        //  rwos/columns 指向事件绑定命中拖动元素  ===============================================================================

        var marked = aggsBox.find(".marked:eq(0)");  // 拖动后的对象事件

        // 全局元素被点击和被拖放后的操作  ========================================================================================


        $(document).click(function (e) { // 弹窗关闭事件
            if ($(e.target).parents(".popover").length === 0) {
                $('.popover').popover('hide');
            }
        });


        //  rwos/columns 添加被拖动域  ==========================================================================================
        var classMapping = {
            "dimension": "columnszone",
            "index": "rowszone"
        };
        function bindDrag(selector) { // 绑定拖动功能
            clearDragover($(selector)[0]).ondrop = function () {
                this.style.borderColor = "#ccc";
                if ($(selector).hasClass(classMapping[hit_drag.class])) {
                    var newMarked = marked.clone(true);
                    newMarked[0].ondragend = function (event) { // 安装拖动后删除事件
                        $(this).remove();
                        event.dataTransfer.clearData("text");
                    };
                    $(selector).append(bingTag(newMarked));
                } else {
                    alert("维度只能拖向Columns,指标只能拖向Rows;请重新配置。")
                }
                return false;
            };

        }

        bindDrag(".columnszone");
        bindDrag(".rowszone");


        // 参数检验 ============================================================================================================
        function checkParams(params) {
            log(params);
            var msg;
            if (!hit_drag.id) {
                msg = "请添加查询条件"
            }
            {#            if (!){#}
            {#                #}
            {#            }#}
            if (!msg) {
                return params
            }
            alert(msg)
        }

        // 预览功能 ============================================================================================================
        var ajaxErrorFunc = function () {
            alert("服务器错误，请联系管理员。")
        };
        function formatBsTable(twoDimensionalArray) {
            var headers = [], body_data = [];
            twoDimensionalArray[0].forEach(function (item) {
                headers.push({
                    field: item,
                    title: item,
                    sortable: true
                })
            });
            twoDimensionalArray.slice(1, twoDimensionalArray.length).forEach(function (row) {
                var cur_row = {};
                headers.forEach(function (item, i) {
                    cur_row[item["field"]] = row[i]
                });
                body_data.push(cur_row)
            });
            return [headers, body_data]
        }
        // 表图切换 =======================================================================================
        var chart = $("#chart-show"), table = $("#table-show").parent();
        $("#form-btn").change(function () {
            if ($(this).is(':checked')) { // 选中时候显示二维表格
                chart.addClass("hidden");
                table.removeClass("hidden");
            } else {
                table.addClass("hidden");
                chart.removeClass("hidden");
            }
        });
        $("#preview").click(function () {
            $('.popover').popover("hide"); // 隐藏所有弹窗
            var zoneMappings = {'filters': '.fliterzone .content', 'rows': '.rowszone', 'columns': '.columnszone'};
            for (var item in zoneMappings) {
                request_params[item] = [];
                $(zoneMappings[item]).children().each(function () {
                    request_params[item].push(updateObject($(this).data("info"), $(this).serializeJson()));
                    // TODO 这里应该对所有的表单添加验证方式
                });
            }
            var data = checkParams(updateObject({
                "source_id": hit_drag.id,
                query: $("#query").val().trim() || "*",
                limit: 0
            }, request_params));  //checkParams();
            var highchartsObject = $(".highed-container");

            if (data) {
                $.ajax({
                    method: "POST",
                    url: "/createchart/preview",
                    data: JSON.stringify(data),
                    dataType: "json",
                    success: function (response) {
                        if (!response.status)
                            alert(response.msg);
                        log(JSON.stringify(response));
                        var response_data = response.data;
                        var csv = [];
                        for (var i = 0; i < response_data.length; i++) {
                            csv.push(response_data[i].join(","));
                        }
                        highchartsObject.find(".tab-body-padded:first .highed-imp-pastearea:eq(0)").val(csv.join("\n")); // 写入csv
                        highchartsObject.find(".highed-imp-button:eq(1)").click(); // 点击预览按钮
                        $("#setting").click();
                        // table
                        var data_table = formatBsTable(response_data);
                        $("#table-show").bootstrapTable({
                            height: 400,
                            toggle: 'table',
                            pagination: true,
                            sidePagination: 'server',
                            columns: data_table[0],
                            data: data_table[1],
                            search: true
                        });
                    },
                    error: ajaxErrorFunc
                });
            }


        });
        $("#setting").click(function () {
            $(".label-active").click() // 自动打开选择图表页面
        });

        // 初始化  ============================================================================================================
        function init() {
            selected_db.trigger("select2-selecting"); // 触发默认选中机制
            selected_db.select2('val', '0'); //  选中第一个
            {#            Highcharts.chart('chart-show', ); 编辑功能的初始化 #}
            highed.ready(function () {
                highed.setLang('zh_cn');
                highed.ModalEditor('setting', {
                    allowDone: true,
                    features: 'import templates customize welcome done',
                    importer: {
                        options: 'plugins csv json samples'
                    }
                }, function (chart) {
                    log(JSON.stringify(chart.export.json()));
                    Highcharts.chart('chart-show', chart.export.json());
                });
            });
        }

        $(function () {
            init()
        });


    </script>

{% endblock %}