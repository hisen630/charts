{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
{% endblock %}
{% block footer %}
    {{ super() }}
    <script> // 扩展
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
    function getObjectFirst(object) {
        for (var item in object) {
            return object[item]
        }
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
    log = console.log;
    </script>
    <script>
        var dbs = {{ dbs | tojson | safe }}, filters = {{ filters | tojson | safe }};
    </script>
    <script type="text/javascript">
        // 标记数据  ===============================================================================================================
        var hit_drag = {}, request_params = {}; // 当前被拖动的对象 请求参数的请求体

        // 维度指标基础  ============================================================================================================
        var index = $('#index'), dimension = $('#dimension');
        function indexDimensionReset(dom1, dom2) { // 重置 维度和指标
            index.empty();
            dimension.empty();
            index.html(dom1);
            dimension.html(dom2);

        }
        // filters 类型映射基础 ============================================================================================================
        var commonType = function () {
            return "<div class='row'>" +
                "<div class='ftitle col-sm-2'>" + hit_drag.text + "</div>" +
                "<div class='col-sm-5' id='c03-select'></div>" +
                "<div class='col-sm-5'><input class='query form-control' placeholder='" + hit_drag.type + "' />" +
                "</div></div>"
        };
        var typesMapping = { // 类型映射
            "number": commonType,
            "string": commonType,
            "date": function (object) {
                return "<div class='row'>" +
                    "<div class='ftitle col-sm-3'>" + hit_drag.text + "</div>" +
                    "<div class='col-sm-4'><input class='form-control' type='date' /></div>" +
                    "<div class='col-sm-1' ><p>到</p></div>" +
                    "<div class='col-sm-4'><input class='form-control' type='date' /></div>" +
                    "</div>"
            }
        };

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
            // indexDimensionReset("", "");
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

        selected_table.on("select2-selecting", function (e) {
            hit_table = dbs[hit_db][((e.object || {}).text || getOneByArray(hit_tables, "id", 0)["text"])];
            var demoIndex = '', demoDimension = '';
            hit_table.index.forEach(function (temp) {
                demoIndex += '<div class="draglist col-sm-6 text-center" data-class="index" data-source="' + temp.source_type + '" data-type="' + temp.type + '" data-field="' + temp.field + '" data-id="' + temp.id + '" draggable="true">' + temp.label + '</div>';
            });
            hit_table.dimension.forEach(function (temp) {
                demoDimension += '<div class="draglist col-sm-6 text-center" data-class="dimension" data-source="' + temp.source_type + '" data-type="' + temp.type + '" data-field="' + temp.field + '" data-id="' + temp.id + '" draggable="true">' + temp.label + '</div>';
            });
            indexDimensionReset(demoIndex, demoDimension);
            refresh_drags();
            columnRowReset();
            filterReset();

        });
        // filter 指向事件绑定命中拖拉元素  ============================================================================================================

        function refresh_drags() {  // 每次点击刷新所有拖动方法
            // 添加操作
            $(".draglist").each(function () {
                this.onselectstart = function () {
                    return false
                };
                this.ondragstart = function (ev) {
                    updateObject(hit_drag, {
                        text: ev.target.innerText,
                        source: ev.target.dataset.source,
                        type: ev.target.dataset.type,
                        id: ev.target.dataset.id,
                        field: ev.target.dataset.field,
                        "class": ev.target.dataset.class
                    }); // 更新数据
                    ev.dataTransfer.effectAllowed = "move";
                    ev.dataTransfer.setData("text", hit_drag);
                    ev.dataTransfer.setDragImage(ev.target, 0, 0);
                    return true;
                };
                this.ondragend = function (ev) {
                    ev.dataTransfer.clearData("text");
                    this.style.borderColor = "#ccc";
                    return false
                };


            });


        }

        // filter 指向事件绑定命中拖拉元素  ============================================================================================================
        function filterReset(html) { // 重置filter
            html = html ? html : "<div class='filter'>filter</div>";
            $(".fliterzone").html(html)
        }
        updateObject($(".fliterzone:eq(0)")[0], {
            ondragover: function (ev) {
                this.style.borderColor = "#56a95b";
                ev.preventDefault();
                return true;
            },
            ondragenter: function (ev) {
                this.style.borderColor = "#56a95b";
                return true;
            },
            ondragleave: function (ev) {
                this.style.borderColor = "#ccc";
                return true;
            },
            ondrop: function (ev) {
                if (filters.operations[hit_drag.source]) {
                    var hit_oper = filters.operations[hit_drag.source][hit_drag.type];
                    $(this).css("border", '1px solid #ccc'); //字典形式
                    $('.fliterzone').html(typesMapping[hit_drag.type]);


                    $("#c03-select").select2({
                        data: function () {
                            var filterSelect = [];
                            for (var item in hit_oper) {
                                filterSelect.push({id: hit_oper[item], 'text': item})
                            }
                            return filterSelect
                        }(),
                        placeholder: 'filter',
                        allowClear: true
                    });
                } else {
                    alert("后台源类型与库类型不匹配(soure type），请联系管理员或自行更改配置!")
                }


                return false;
            }
        });
        // 维度指标被拖拉后产生的标签 ========================================================================================

        function bingTag(tag) {
            return updateObject(tag, {
                ondragleave: function (event) {

                }
            })
        }

        //  rwos/columns 指向事件绑定命中拖拉元素  ============================================================================================================
        var classMapping = {
            dimension: "columnszone",
            index: "rowszone"
        };

        function bindDrag(selector) { // 绑定拖拉功能
            return updateObject($(selector)[0], {
                ondragover: function (ev) {
                    this.style.borderColor = "#56a95b";
                    ev.preventDefault();
                    return true;
                },
                ondragenter: function (ev) {
                    this.style.borderColor = "#56a95b";
                    return true;
                },
                ondragleave: function (ev) {
                    this.style.borderColor = "#ccc";
                    return true;
                },

                ondrop: function (ev) {
                    this.style.borderColor = "#ccc";
                    var hit = $(selector);
                    if (hit.hasClass(classMapping[hit_drag.class])) {
                        var tag = $("<div class='itemlist' data-name='" + hit_drag.field + "'> " + hit_drag.text + "<p></p></div>");
                        hit.find(".cr").append(bingTag(tag));
                        hit.on('click', '.itemlist', function (event) {
                            $(this).remove(); // 清除本身
                            event.preventDefault();
                        });
                    } else {
                        alert("维度只能拖向Columns,指标只能拖向Rows;请重新配置。")
                    }

                    return false;
                }
            })
        }


        var columns = $(".columnszone"), rows = $(".rowszone");
        bindDrag(".columnszone");
        bindDrag(".rowszone");
        function columnRowReset() { // 重置准备提交的内容
            columns.html('<div class="cr">Columns</div>');
            rows.html('<div class="cr">Rows</div>')
        }


        // 预览功能 ============================================================================================================
        $(".preview:eq(0)").click(function () {
            request_params.columns = [], request_params.rows = [];
            columns.find(".itemlist").each(function () {
                request_params.columns.push($(this).data("name"));
            });
            rows.find(".itemlist").each(function () {
                request_params.rows.push($(this).data("name"));
            });
            log(request_params)
        });

        // 保存功能 ============================================================================================================


        // 初始化  ============================================================================================================
        function init() {
            selected_db.trigger("select2-selecting"); // 触发默认选中机制
            selected_db.select2('val', '0'); // select2 选中第一个

        }

        $(function () {
            init()
        });


    </script>
{% endblock %}
{% block content %}
    <style type="text/css">
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

        ::-webkit-input-placeholder { /* WebKit browsers */
            color: #ccc;
            text-align: center;
        }

        :-moz-placeholder { /* Mozilla Firefox 4 to 18 */
            color: #ccc;
            text-align: center;
        }

        ::-moz-placeholder { /* Mozilla Firefox 19+ */
            color: #ccc;
            text-align: center;
        }

        :-ms-input-placeholder { /* Internet Explorer 10+ */
            color: #ccc;
            text-align: center;
        }

        li {
            list-style-type: none
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

        .drapbox {
            color: #999;
            padding: 4px 5px;
            margin-bottom: 3px;
            border: 1px solid #ccc;
            font-size: 12px;
            height: auto;
            overflow: hidden;
            margin-top: 1px;
            /*cursor: move;*/
            /*height: 36px;*/
            /*line-height: 36px;*/
        }

        .filter {
            text-align: center;
            color: #ccc;
            height: 40px;
            line-height: 40px;
        }

        .ftitle {
            color: #666;
            font-size: 14px;
            text-align: center;
        }

        .itemlist {
            text-align: center;
            color: #999;
            height: 24px;
            line-height: 24px;
            padding: 0 5px;
            margin: 4px;
            float: left;
            background-color: #bbb;
            color: #fff;
            border-radius: 2px;
            /*border: 1px solid #999;*/
            cursor: pointer;
        }

        .endbox {
            color: #666;
            padding: 0 5px;
            margin-bottom: 3px;
            border: 1px solid #ccc;
            font-size: 12px;
            height: auto;
            overflow: hidden;
            height: 34px;
            line-height: 34px;
            text-align: center;
        }

        .cr {
            color: #ccc
        }

        .itemlist:after {
            content: 'X';
            color: #666;
            padding: 2px;
        }


    </style>

    <div class="row">
        <div class="col-sm-3">
            <div id="c01-select" class="form-control"></div>
            <div id="c02-select" class="form-control"></div>
            <div>
                <input class='form-control' type='text' placeholder='Query(默认为*)'/>
            </div>
            <fieldset>
                <legend>维度</legend>
                <div id="dimension" class="row"></div>
            </fieldset>
            <fieldset>
                <legend>指标</legend>
                <div id="index" class='dragbox row'></div>
            </fieldset>
        </div>
        <div class="col-sm-9">
            <div>
                <div class='fliterzone drapbox row' draggable="false">
                    <div class='filter'>filter</div>
                </div>
                <div class="row">
                    <div class='columnszone endbox'>
                        <div class='cr'>columns</div>
                    </div>
                    <div class='rowszone endbox'>
                        <div class='cr'>rows</div>
                    </div>

                </div>
            </div>
            <div class="row">
                <div class="col-sm-6"></div>
                <div class="col-sm-6">
                    <button class="preview btn btn-sm btn-block">预览</button>
                </div>

            </div>
        </div>

    </div>

{% endblock %}
