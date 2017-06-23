{% extends "layouts/nav.tpl" %}
{% block header %}
    {{ super() }}
{% endblock %}
{% block footer %}
    {{ super() }}
    <script type="text/javascript">
    	$(function(){
    		Array.prototype.indexOf = function(val) {
			for (var i = 0; i < this.length; i++) {
			if (this[i] == val) return i;
			}
			return -1;
			};
			Array.prototype.remove = function(val) {
			var index = this.indexOf(val);
			if (index > -1) {
			this.splice(index, 1);
			}
			};
			Array.prototype.unique = function(){
			 var res = [];
			 var json = {};
			 for(var i = 0; i < this.length; i++){
			  if(!json[this[i]]){
			   res.push(this[i]);
			   json[this[i]] = 1;
			  }
			 }
			 return res;
			}

    		var dataArr = {
				    "hi-prod-19:9200@online_taobao_*_*-*-*": {
				        "item_list": {
				            "index": [
				                {
				                    "field": "gmv",
				                    "source_type": 4,
				                    "type": "number",
				                    "id": 2,
				                    "label": "销量"
				                }
				            ],
				            "dimension": [
				                {
				                    "field": "ctime",
				                    "source_type": 4,
				                    "type": "date",
				                    "id": 2,
				                    "label": "时间"
				                },
				                {
				                    "field": "name",
				                    "source_type": 4,
				                    "type": "string",
				                    "id": 2,
				                    "label": "名称"
				                }
				            ]
				        }
				    },
				    "127.0.0.1:9999@online_taobao_*_*-*-*": {
				        "item_list": {
				            "index": [
				                {
				                    "field": "month_sale",
				                    "source_type": 4,
				                    "type": "number",
				                    "id": 1,
				                    "label": "月销售"
				                },
				                {
				                    "field": "gmv",
				                    "source_type": 4,
				                    "type": "number",
				                    "id": 1,
				                    "label": "销量"
				                }
				            ],
				            "dimension": [
				                {
				                    "field": "fg_category2_name.raw",
				                    "source_type": 4,
				                    "type": "terms",
				                    "id": 1,
				                    "label": "二级分类"
				                },
				                {
				                    "field": "fg_category3_name.raw",
				                    "source_type": 4,
				                    "type": "terms",
				                    "id": 1,
				                    "label": "三级分类"
				                }
				            ]
				        }
				    },
				    "localhost@god_metric_meta2": {
				        "t_chart_test_data": {
				            "index": [
				                {
				                    "field": "gmv",
				                    "source_type": 0,
				                    "type": "number",
				                    "id": 4,
				                    "label": "销量"
				                },
				                {
				                    "field": "gmv",
				                    "source_type": 0,
				                    "type": "number",
				                    "id": 5,
				                    "label": "销量"
				                }
				            ],
				            "dimension": [
				                {
				                    "field": "ctime",
				                    "source_type": 0,
				                    "type": "date",
				                    "id": 4,
				                    "label": "时间"
				                },
				                {
				                    "field": "name",
				                    "source_type": 0,
				                    "type": "string",
				                    "id": 4,
				                    "label": "名称"
				                }
				            ]
				        }
				    },
				    "localhost@god_metric_meta1": {
				        "t_chart_test_data": {
				            "index": [
				                {
				                    "field": "gmv",
				                    "source_type": 0,
				                    "type": "number",
				                    "id": 3,
				                    "label": "销量"
				                }
				            ],
				            "dimension": [
				                {
				                    "field": "ctime",
				                    "source_type": 0,
				                    "type": "date",
				                    "id": 3,
				                    "label": "时间"
				                },
				                {
				                    "field": "name",
				                    "source_type": 0,
				                    "type": "string",
				                    "id": 3,
				                    "label": "名称"
				                }
				            ]
				        }
				    }
				}

			var filter = {
				"0": {"number": {">=": 1, "==": 3, "<=": 2, "!=": 4, "<": 6, ">": 5}, "string": {"%{}%": 10, "{}%": 12, "{}*": 13, "*{}": 14, "*{}*": 15, "%{}": 11}},
				"2": {"number": {">=": 1, "==": 3, "<=": 2, "!=": 4, "<": 6, ">": 5}, "string": {"%{}%": 10, "{}%": 12, "{}*": 13, "*{}": 14, "*{}*": 15, "%{}": 11}},
				"1": {"number": {">=": 1, "==": 3, "<=": 2, "!=": 4, "<": 6, ">": 5}, "string": {"%{}%": 10, "{}%": 12, "{}*": 13, "*{}": 14, "*{}*": 15, "%{}": 11}},
				"4": {"number": {">=": 1, "==": 3, "<=": 2, "!=": 4, "<": 6, ">": 5}, "string": {"%{}%": 10, "{}%": 12, "{}*": 13, "*{}": 14, "*{}*": 15, "%{}": 11}}
				}		

			var sum = {
					"0":[
						{
						name: "sum",
						label: "求和"
						},
						{
						name: "max",
						label: "求最大"
						},
						{
						name: "min",
						label: "求最小"
						}
						],
					"4": [
						{
						name: "sum",
						label: "求和"
						},
						{
						name: "max",
						label: "求最大"
						},
						{
						name: "min",
						label: "求最小"
						}
					]	
				}
    		
    		var dbArr = [],tbArr = [],sdb='',i=0
    		for (item in dataArr){
				dbArr.push({id:i,'text':item}),
				i+=1
			}


			$("#c01-select").select2({
				data: dbArr,
			 	placeholder:'选择库',
  				allowClear:true
			})

			$("#c01-select").select2('val','0')

			$("#c01-select").on("select2-selecting", function (e) {
				sdb = e.object.text
				tbArr.splice(0,tbArr.length);
				var j = 0
	    		for (item in dataArr[e.object.text]){
					tbArr.push({id:j,'text':item}),
					j+=1
				}
			});

			$("#c02-select").select2({
				data: tbArr,
			 	placeholder:'选择表',
  				allowClear:true,
			})

			$("#c02-select").select2('val','0')

			$("#c02-select").on("select2-selecting", function (e) {
				var select = dataArr[sdb][e.object.text]
				// console.log(select)
				$('#index').empty()
				$('#dimension').empty()
				var demoIndex = '',demoDimension = ''
				for (var i = 0; i < select.index.length; i++) {
					var si = select.index[i]
					demoIndex+='<div class="draglist" data-source="'+si.source_type+'" data-type="'+si.type+'" data-field="'+si.field+'" data-id="'+si.id+'" draggable="true">'+si.label+'</div>'

					var sd = select.dimension[i]
					demoDimension+='<div class="draglist" data-source="'+sd.source_type+'" data-type="'+sd.type+'" data-field="'+sd.field+'" data-id="'+sd.id+'" draggable="true">'+sd.label+'</div>'
				};
				$('#index').html(demoIndex)
				$('#dimension').html(demoDimension)


				var fliterzone = $(".fliterzone")[0], 
					sumzone = $(".sumzone")[0], 
					columnszone = $(".columnszone")[0],
					rowszone = $('.rowszone')[0],

					eleDrags = $(".draglist"), 
					lDrags = eleDrags.length,  

					eleDrag = null, //filter数据
					evesum =null, // sum数据

					ifsum =false,
					ifrows = false,
					ifcolumns = false;

				//拖动左侧列表	
				for (var i=0; i<lDrags; i+=1) {
					eleDrags[i].onselectstart = function() {
						return false;
					};
					eleDrags[i].ondragstart = function(ev) {
						var eleobj = {}//list数据
						eleobj.text = ev.target.innerText
						eleobj.source = ev.target.dataset.source
						eleobj.type = ev.target.dataset.type
						eleobj.id = ev.target.dataset.id
						eleobj.field = ev.target.dataset.field

						if (eleobj.type == 'number') {
							ifsum = true
						} else{
							ifsum = false
						};

						if (eleobj.type) {
							ifcolumns = true
						} else{
							ifcolumns = false
						};

						ev.dataTransfer.effectAllowed = "move";
						ev.dataTransfer.setData("text", eleobj);
						ev.dataTransfer.setDragImage(ev.target, 0, 0);
						eleDrag = eleobj
						return true;
					};
					eleDrags[i].ondragend = function(ev) {
						ev.dataTransfer.clearData("text");
						this.style.borderColor = "#ccc";
						eleDrag = null;
						ifsum = false;
						ifcolumns =false;
						return false
					};
				}

				//拖入filter
				fliterzone.ondragover = function(ev) {
					this.style.borderColor = "#56a95b";
					ev.preventDefault();
					return true;
				};

				fliterzone.ondragenter = function(ev) {
					this.style.borderColor = "#56a95b";
					return true;
				};
				fliterzone.ondragleave = function(ev) {
					this.style.borderColor = "#ccc";
					return true;
				}
				fliterzone.ondrop = function(ev) {
					$(this).css({
						border: '1px solid #ccc',
						// cursor:'move'
					});
					// $(this).attr('draggable', 'true');

					var source_obj = {}
					for (source_type in filter) {
						source_obj = filter[eleDrag.source]
					}	
					console.log(source_obj)

					var type_obj = {}
					for (type in source_obj){
						type_obj = source_obj[eleDrag.type]
					}
					console.log(type_obj)

					if (eleDrag.type == 'date') {
						var demol = "<div class='pdt10 ftitle col-md-2'>"+eleDrag.text+"</div>"+
										"<input class='query' type='"+eleDrag.type+"' />"+
										"<input class='query' type='"+eleDrag.type+"' />"
					} else{
						var demol = "<div class='pdt10 ftitle col-md-2'>"+eleDrag.text+"</div>"+
									"<div class='fq' id='c03-select'></div>"+
									"<div class='col-md-6'>"+
										"<input class='query' placeholder='"+eleDrag.type+"' />"+
									"</div>"
					};

					
					$('.fliterzone').html(demol)

					var querySelect = []
					for (items in type_obj){
						querySelect.push({id:type_obj[items],'text':items})
					}

					var $example3 = $("#c03-select").select2({
						data: querySelect,
					 	placeholder:'filter',
		  				allowClear:true,
					})
					
					return false;
				};

				

				//拖入sum
				sumzone.ondragover = function(ev) {
					ev.preventDefault();
					if (ifsum) {
						this.style.borderColor = "#56a95b";
					} 
					return true;
				};

				sumzone.ondragenter = function(ev) {
					if (ifsum) {
						this.style.borderColor = "#56a95b";
					} 
					return true;
				};
				sumzone.ondragleave = function(ev) {
					this.style.borderColor = "#ccc";
					return true;
				}
				sumzone.ondrop = function(ev) {

					if (ifsum) {
						$(this).css({
							border: '1px dashed #ccc',
							cursor:'move'
						});
						$(this).attr('draggable', 'true');
						var sumdemo = "<div class='pdt10 ftitle col-md-2'>"+eleDrag.text+"</div><div class='fq' id='c04-select'></div>"
					
						$('.sumzone').html(sumdemo)

						var sum_arr = []
						for (sum_type in sum) {
							sum_arr = sum[eleDrag.source]
						}

						var sumSelect = []
						for (var i = 0; i < sum_arr.length; i++) {
							sumSelect.push({'id':sum_arr[i].name,'text':sum_arr[i].label})
						};

						console.log(sumSelect)
						$("#c04-select").select2({
							data: sumSelect,
						 	placeholder:'sum',
			  				allowClear:true,
						})
					} 
					return false;
				};


				//拖动sum
				sumzone.onselectstart = function() {
					return false;
				};
				sumzone.ondragstart = function(ev) {
					ifrows = true;
					ifcolumns = false
					var sum_ojb = {}
					sum_ojb.sumname = $(this).find('.ftitle').text()+'-'+$(this).find('.select2-chosen').text()
					sum_ojb.sumval = $("#c04-select").find("option:selected").val()
					
					console.log(sum_ojb)

					ev.dataTransfer.effectAllowed = "move";
					ev.dataTransfer.setData("text", sum_ojb);
					ev.dataTransfer.setDragImage(ev.target, 0, 0);
					evesum = sum_ojb
					return true;
				};
				sumzone.ondragend = function(ev) {
					ev.dataTransfer.clearData("text");
					this.style.borderColor = "#ccc";
					// evearr.remove(eve)
					evesum = null;
					ifrows = false;
					return false
				};


				//拖入rows
				rowszone.ondragover = function(ev) {
					if (ifrows) {
						this.style.borderColor = "#56a95b";
					}
					ev.preventDefault();
					return true;
				};

				rowszone.ondragenter = function(ev) {
					if (ifrows) {
						this.style.borderColor = "#56a95b";
					}
					return true;
				};
				rowszone.ondragleave = function(ev) {
					this.style.borderColor = "#ccc";
					return true;
				}
				rowszone.ondrop = function(ev) {
					if (ifrows) {
						this.style.borderColor = "#ccc";
							
						$('.rowszone').html('<div class="itemlist">'+evesum.sumname+'</div>')

						$('.rowszone').on('click', '.itemlist', function(event) {
							event.preventDefault();
							evesum = null
							$('.rowszone').html('<div class="cr">rows</div>')

						});
						return false;
					} else{
						console.log(11)
						this.style.borderColor = "#ccc";
						return false;
					};
		
				};


				//拖入colnums
				columnszone.ondragover = function(ev) {
					if (ifcolumns) {
						this.style.borderColor = "#56a95b";
					}
					ev.preventDefault();
					return true;
				};

				columnszone.ondragenter = function(ev) {
					if (ifcolumns) {
						this.style.borderColor = "#56a95b";
					}
					return true;
				};
				columnszone.ondragleave = function(ev) {
					this.style.borderColor = "#ccc";
					return true;
				}
				columnszone.ondrop = function(ev) {
					if (ifcolumns) {
						this.style.borderColor = "#ccc";
						$('.columnszone').html('<div class="itemlist">'+eleDrag.text+'</div>')

						$('.columnszone').on('click', '.itemlist', function(event) {
							event.preventDefault();
							eleDrag = null
							$('.columnszone').html('<div class="cr">columns</div>')

						});
						return false;
					} else{
						console.log(11)
						this.style.borderColor = "#ccc";
						return false;
					};
		
				};

			});
			

			
			// $("#c05-select").on("select2-removed", function (e) {
			// 	DropzoneArr.remove(e.val)
			// 	console.log(DropzoneArr)
			// });

    	})
    	
    </script>
{% endblock %}
{% block content %}
<style type="text/css">

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
	.pdt10{
		padding-top: 6px;
	}
	.row-fluid{ margin: -25px -30px; padding:15px 0; font-size: 14px; background-color: #fff; height: auto; overflow: hidden;}
	#s2id_c01-select{
		min-width: 100px;
		margin-bottom: 10px
	}
	li{ list-style-type: none}
	.draglist{
		padding:4px 5px;
	    margin-bottom: 3px;
	    border: 1px dashed #ccc;
	    cursor: move;
	    font-size: 12px
	}
	.draglist:hover {
	    border-color: #cad5eb;
	    background-color: #eee;
	}
	.drapbox{
		color: #999;
		padding:4px 5px;
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
	.querydiv{
		color: #666;
		padding:0 5px;
	    margin-bottom: 3px;
	    border: 1px solid #ccc;
	    font-size: 12px;
	    height: auto; 
	    overflow: hidden;
	    height: 34px; 
	    line-height: 34px; 
	    text-align: center;
	}
	.querydiv input{
		border: none;
		width: 100%;
		outline: none
	}

	.filter{
		text-align: center;
		color: #ccc;
		height: 40px;
		line-height: 40px;
	}
	.ftitle{
		color: #666;
		font-size: 14px;
		/*width: 50px;
		float: left;*/
		text-align: center;
	}
	.fq{
		width: 200px;
		float: left;
	}
	.query{
		color: #666;
		height: 34px;
		border-radius: 4px;
		border: 1px solid #ccc;
		box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
	}
	.qu{
		color: #666;
		height: 35px;
		margin-bottom: 3px;
		border: 1px solid #ccc;
	}
	.sum{
		margin-left: 10px;
		width: 200px;
		float: left;
		color: #666;
		height: 34px;
		line-height: 34px;
		border-radius: 4px;
		border: 1px solid #ccc;
	}
	.w200{
		width:200px;
		float: left;
		margin-left: -15px;
	}
	.endbox{

	}

	.itemlist{
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

	.endbox{
		color: #666;
		padding:0 5px;
	    margin-bottom: 3px;
	    border: 1px solid #ccc;
	    font-size: 12px;
	    height: auto; 
	    overflow: hidden;
	    height: 34px; 
	    line-height: 34px; 
	    text-align: center;
	}
	.cr{
		color: #ccc
	}

	.itemlist:after{
		content: 'X';
		color: #666;
		padding: 2px;
	};

	
</style>
<div class="row-fluid">
	<div class="col-md-4">
        <div id="c01-select"></div>
        <div id="c02-select"></div>
	    <h5 class="text-center" id=''>维度</h5>
	    <div id="dimension">
	    </div>
	    <h5 class="text-center" id=''>指标</h5>
        <div id="index" class='dragbox'>
	    </div>

	</div>
	<div class="col-md-8">
		<div class="col-md-12">
			
			<div class='col-md-12 querydiv' draggable="false">
				<input class='' type='text' placeholder='query' />
			</div>

			<div class='fliterzone drapbox col-md-12' draggable="false">
				<div class='filter'>filter</div>
			</div>
			<div class='sumzone drapbox col-md-12' draggable="false">
				<div class='filter'>sum</div>
			</div>
		</div>

		<div class="col-md-12">
			<div class='columnszone endbox col-md-12'>
				<div class='cr'>columns</div>
			</div>
			<div class='rowszone endbox col-md-12'>
				<div class='cr'>rows</div>
			</div>

		</div>
		
	</div>
	
</div>
</div>
{% endblock %}
