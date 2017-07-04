/******************************************************************************

Copyright (c) 2016, Highsoft

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

******************************************************************************/

if (typeof highed === 'undefined') {
	var highed = {meta: {}};
}

highed.meta.chartTemplates = {
	line: {
		title: '线图',
		templates: {
			basic: {
				title: '直线图',
				urlImg: 'https://cloud.highcharts.com/images/abywon/0/136.svg',
				config: {
					'chart--type': 'line',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			withdatalabel: {
				title: '数据标签',
				urlImg: 'https://cloud.highcharts.com/images/agonam/2/136.svg',
				config: {
					'chart--type': 'line',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values. ' +
				'Data labels by default displays the Y value.'
			},
			spline: {
				title: '曲线图',
				urlImg: 'https://cloud.highcharts.com/images/upafes/1/136.svg',
				config: {
					'chart--type': 'spline',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			splineWithDataLabel: {
				title: '曲线图，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/odopic/2/136.svg',
				config: {
					'chart--type': 'spline',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			logarithmic: {
				title: '对数图',
				urlImg: 'https://cloud.highcharts.com/images/abywon/0/136.svg',
				config: {
					'chart--type': 'line',
					'yAxis--type': 'logarithmic',
					'yAxis--minorTickInterval': 'auto',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			stepLine: {
				title: '阶梯图',
				urlImg: 'https://cloud.highcharts.com/images/akeduw/0/136.svg',
				config: {
					'chart--type': 'line',
					'plotOptions-line--step': 'left',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			stepLineWithDataLabel: {
				title: '阶梯图，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/oxenux/0/136.svg',
				config: {
					'chart--type': 'line',
					'plotOptions-series-dataLabels--enabled': true,
					'plotOptions-line--step': 'left',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			inverted: {
				title: '坐标轴反转',
				urlImg: 'https://cloud.highcharts.com/images/ozojul/1/136.svg',
				config: {
					'chart--type': 'line',
					'chart--inverted': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			negative: {
				title: '正负值不同颜色',
				urlImg: 'https://cloud.highcharts.com/images/uxyfys/2/136.svg',
				config: {
					'chart--type': 'line',
					'series[0]--negativeColor': '#0088FF',
					'series[0]--color': '#FF0000',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			errorbar: {
				title: '误差线图',
				urlImg: 'https://cloud.highcharts.com/images/ypewak/0/136.svg',
				config: {
					'chart--type': 'line',
					'series[0]--type': 'line',
					'series[1]--type': 'errorbar',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for the series\' Y values. ' +
				'and two columns for the error bar series maximum and minimum.'
			},
			combination: {
				title: '组合图',
				urlImg: 'https://cloud.highcharts.com/images/ynikoc/0/136.svg',
				config: {
					'chart--type': 'line',
					'series[0]--type': 'column',
					'chart--polar': false
				},
				tooltipText: 'Requires two data columns.'
			}
		}
	},
	area: {
		title: '面积图',
		templates: {
			basic: {
				title: '基础面积图',
				urlImg: 'https://cloud.highcharts.com/images/ecexev/2/136.svg',
				config: {
					'chart--type': 'area',
					'chart--polar': false
				},
				tooltipText: 'Non-stacked area chart. Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			basicDatalabels: {
				title: '数据标签',
				urlImg: 'https://cloud.highcharts.com/images/atikon/0/136.svg',
				config: {
					'chart--type': 'area',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Non-stacked area chart with data labels. Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			stacked: {
				title: '堆叠面积图',
				urlImg: 'https://cloud.highcharts.com/images/inebav/1/136.svg',
				config: {
					'chart--type': 'area',
					'plotOptions-series--stacking': 'normal',
					'chart--polar': false
				},
				tooltipText: 'Stacked area chart. Requires one column for X values or categories, subsequently one column for each series\' Y values. ' +
				'The first data series is in the top of the stack.'
			},
			stackedDatalabels: {
				title: '堆叠面积图，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/iluryh/0/136.svg',
				config: {
					'chart--type': 'area',
					'plotOptions-series--stacking': 'normal',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Stacked area chart. Requires one column for X values or categories, subsequently one column for each series\' Y values. ' +
				'The first data series is in the top of the stack.'
			},
			percentage: {
				title: '百分比堆叠',
				urlImg: 'https://cloud.highcharts.com/images/iporos/1/136.svg',
				config: {
					'chart--type': 'area',
					'plotOptions-series--stacking': 'percent',
					'chart--polar': false
				},
				tooltipText: 'Stacked percentage area chart. Requires one column for X values or categories, subsequently one column for each series\' Y values. ' +
				'The first data series is in the top of the stack.'
			},
			inverted: {
				title: '坐标轴反转',
				urlImg: 'https://cloud.highcharts.com/images/yqenid/0/136.svg',
				config: {
					'chart--type': 'area',
					'chart--inverted': true,
					'chart--polar': false
				},
				tooltipText: 'Area chart with inverted axes. Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			invertedDatalabels: {
				title: '坐标轴反转，显示标签',
				urlImg: 'https://cloud.highcharts.com/images/acemyq/0/136.svg',
				config: {
					'chart--type': 'area',
					'chart--inverted': true,
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Area chart with inverted axes and data labels. Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			stepLine: {
				title: '阶梯图',
				urlImg: 'https://cloud.highcharts.com/images/abutix/0/136.svg',
				config: {
					'chart--type': 'area',
					'plotOptions-area--step': 'left',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			negative: {
				title: '正负值不同颜色',
				urlImg: 'https://cloud.highcharts.com/images/ydypal/0/136.svg',
				config: {
					'chart--type': 'area',
					'series[0]--negativeColor': '#0088FF',
					'series[0]--color': '#FF0000',
					'chart--polar': false
				},
				tooltipText: 'Displays negative values with an alternative color. Colors can be set in Customize -> Simple -> Data series. Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			arearange: {
				title: '面积范围图',
				urlImg: 'https://cloud.highcharts.com/images/udepat/0/136.svg',
				config: {
					'chart--type': 'arearange',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently two data column for each arearange series\' Y values.'
			}
		}
	},
	column: {
		title: '柱状图',
		templates: {
			grouped: {
				title: '基础柱状图',
				urlImg: 'https://cloud.highcharts.com/images/ovobiq/1/136.svg',
				config: {
					'chart--type': 'column',
					'chart--polar': false
				},
				tooltipText: 'Grouped column chart. Requires one data column for X values or categories, subsequently one data column for each series\' Y values.'
			},
			groupedLabels: {
				title: '数据标签',
				urlImg: 'https://cloud.highcharts.com/images/ivetir/1/136.svg',
				config: {
					'chart--type': 'column',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Grouped column chart with datalabels. Requires one data column for X values or categories, subsequently one data column for each series\' Y values.'
			},
			column3d: {
				title: '3D 柱状图',
				urlImg: 'https://cloud.highcharts.com/images/ahyqyx/1/136.svg',
				config: {
					'chart--type': 'column',
					'chart--margin': 75,
					'chart-options3d--enabled': true,
					'chart-options3d--alpha': 15,
					'chart-options3d--beta': 15,
					'chart-options3d--depth': 50,
					'chart-options3d--viewDistance': 15,
					'plotOptions-column--depth': 25,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values.'
			},
			columnstacked: {
				title: '堆叠柱状图',
				urlImg: 'https://cloud.highcharts.com/images/ycehiz/1/136.svg',
				config: {
					'chart--type': 'column',
					'plotOptions-series--stacking': 'normal',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values.'
			},
			columnstackedLabels: {
				title: '堆叠，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/acijil/0/136.svg',
				config: {
					'chart--type': 'column',
					'plotOptions-series--stacking': 'normal',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values.'
			},
			columnStacked3d: {
				title: '3D 堆叠',
				urlImg: 'https://cloud.highcharts.com/images/ahyqyx/1/136.svg',
				config: {
					'chart--type': 'column',
					'chart--margin': 75,
					'chart-options3d--enabled': true,
					'chart-options3d--alpha': 15,
					'chart-options3d--beta': 15,
					'chart-options3d--depth': 50,
					'chart-options3d--viewDistance': 15,
					'plotOptions-column--depth': 25,
					'plotOptions-series--stacking': 'normal',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values.'
			},
			columnStackedPercentage: {
				title: '百分比堆叠',
				urlImg: 'https://cloud.highcharts.com/images/ojixow/0/136.svg',
				config: {
					'chart--type': 'column',
					'plotOptions-series--stacking': 'percent'
				},
				tooltipText: 'Grouped column chart. Requires one data column for X values or categories, subsequently one data column for each series\' Y values.'
			},
			columnStackedPercentageLabels: {
				title: '百分比堆叠，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/iwanyg/0/136.svg',
				config: {
					'chart--type': 'column',
					'plotOptions-series--stacking': 'percent',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Grouped column chart. Requires one data column for X values or categories, subsequently one data column for each series\' Y values.'
			},
			negative: {
				title: '正负值不同颜色',
				urlImg: 'https://cloud.highcharts.com/images/yxajih/0/136.svg',
				config: {
					'chart--type': 'column',
					'series[0]--negativeColor': '#0088FF',
					'series[0]--color': '#FF0000',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			multiColor: {
				title: '多颜色',
				urlImg: 'https://cloud.highcharts.com/images/alyqyz/0/136.svg',
				config: {
					'chart--type': 'column',
					'plotOptions-series--colorByPoint': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			logarithmic: {
				title: '极坐标',
				urlImg: 'https://cloud.highcharts.com/images/igipeg/0/136.svg',
				config: {
					'chart--type': 'column',
					'yAxis--type': 'logarithmic',
					'yAxis--minorTickInterval': 'auto',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			columnrange: {
				title: '柱状范围图',
				urlImg: 'https://cloud.highcharts.com/images/ihilaq/0/136.svg',
				config: {
					'chart--type': 'columnrange',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'two data column for each series\' Y values (horizontal axis).'
			},
			columnrangeLabelsLabels: {
				title: '范围图，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/ojykiw/0/136.svg',
				config: {
					'chart--type': 'columnrange',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'two data column for each series\' Y values (horizontal axis).'
			},
			packedColumns: {
				title: '紧凑的柱状图',
				urlImg: 'https://cloud.highcharts.com/images/exypor/0/136.svg',
				config: {
					'chart--type': 'column',
					'plotOptions-series--pointPadding': 0,
					'plotOptions-series--groupPadding': 0,
					'plotOptions-series--borderWidth': 0,
					'plotOptions-series--shadow': false,
					'chart--polar': false
				},
				tooltiptext: 'Requires one data column for X values or categories, subsequently one data column for the series\' Y values.'
			},
			errorbar: {
				title: '误差线',
				urlImg: 'https://cloud.highcharts.com/images/icytes/0/136.svg',
				config: {
					'chart--type': 'column',
					'series[1]--type': 'errorbar',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for the series\' Y values. and two columns for the error bar series maximum and minimum.'
			}
		}
	},
	bar: {
		title: '条形图',
		templates: {
			basic: {
				title: '基础条形图',
				urlImg: 'https://cloud.highcharts.com/images/ovuvul/1/137.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			basicLabels: {
				title: '数据标签',
				urlImg: 'https://cloud.highcharts.com/images/ovuvul/1/137.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			barstacked: {
				title: '堆叠',
				urlImg: 'https://cloud.highcharts.com/images/epodat/3/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'plotOptions-series--stacking': 'normal',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			barstackedLabels: {
				title: '堆叠，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/otupaz/1/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'plotOptions-series--stacking': 'normal',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			barstackedpercentage: {
				title: '百分比堆叠',
				urlImg: 'https://cloud.highcharts.com/images/yhekaq/2/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'plotOptions-series--stacking': 'percent',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			barstackedpercentageLabels: {
				title: '百分比堆叠，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/izoqyx/0/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'plotOptions-series--stacking': 'percent',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			negative: {
				title: '正负值不同颜色',
				urlImg: 'https://cloud.highcharts.com/images/efygam/0/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'series[0]--negativeColor': '#0088FF',
					'series[0]--color': '#FF0000',
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			multiColor: {
				title: '多颜色',
				urlImg: 'https://cloud.highcharts.com/images/ogixak/0/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'plotOptions-series-colorByPoint': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			logarithmic: {
				title: '对数图',
				urlImg: 'https://cloud.highcharts.com/images/imykus/0/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'yAxis--type': 'logarithmic',
					'yAxis--minorTickInterval': 'auto',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'one data column for each series\' Y values (horizontal axis).'
			},
			barRange: {
				title: '水平范围图',
				urlImg: 'https://cloud.highcharts.com/images/iqagel/0/136.svg',
				config: {
					'chart--type': 'columnrange',
					'chart--inverted': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'two data column for each series\' Y values (horizontal axis).'
			},
			barRangeLabels: {
				title: '范围图，数据标签',
				urlImg: 'https://cloud.highcharts.com/images/eracar/0/136.svg',
				config: {
					'chart--type': 'columnrange',
					'chart--inverted': true,
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories (vertical axis), subsequently ' +
				'two data column for each series\' Y values (horizontal axis).'
			},
			packedColumns: {
				title: '紧凑的条形图',
				urlImg: 'https://cloud.highcharts.com/images/orixis/0/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'plotOptions-series--pointPadding': 0,
					'plotOptions-series--groupPadding': 0,
					'plotOptions-series--borderWidth': 0,
					'plotOptions-series--shadow': false,
					'chart--polar': false
				},
				tooltiptext: 'Requires one data column for X values or categories, subsequently one data column for the series\' Y values.'
			},
			errorbar: {
				title: '误差线',
				urlImg: 'https://cloud.highcharts.com/images/omikax/0/136.svg',
				config: {
					'chart--type': 'column',
					'chart--inverted': true,
					'series[1]--type': 'errorbar',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for the series\' Y values. and two columns for the error bar series maximum and minimum.'
			}
		}
	},
	scatterandbubble: {
		title: '散点图及气泡图',
		templates: {
			scatter: {
				title: '散点图',
				urlImg: 'https://cloud.highcharts.com/images/ezatat/0/136.svg',
				config: {
					'chart--type': 'scatter',
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values and one for Y values.'
			},
			bubbles: {
				title: '气泡图',
				urlImg: 'https://cloud.highcharts.com/images/usyfyw/0/136.svg',
				config: {
					'chart--type': 'bubble',
					'chart--polar': false
				},
				tooltipText: 'Requires three data columns: one for X values, one for Y values and one for the size of the bubble (Z value).'
			},
			scatterLine: {
				title: '趋势线、散点',
				urlImg: 'https://cloud.highcharts.com/images/ydaqok/0/136.svg',
				config: {
					'chart--type': 'scatter',
					'plotOptions-series--lineWidth': 1,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values and one for Y values.'
			},
			scatterLineNoMarker: {
				title: 'Scatter with line, no marker',
				urlImg: 'https://cloud.highcharts.com/images/uvepiw/0/136.svg',
				config: {
					'chart--type': 'scatter',
					'plotOptions-series--lineWidth': 1,
					'plotOptions-series-marker--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Requires one data column for X values and one for Y values.'
			}
		}
	},
	pie: {
		title: '饼图',
		templates: {
			pie: {
				title: '基础饼图',
				urlImg: 'https://cloud.highcharts.com/images/yqoxob/3/136.svg',
				config: {
					'chart--type': 'pie',
					'plotOptions-pie--allowPointSelect': true,
					'plotOptions-pie--cursor': true,
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires two data columns: one for slice names (shown in data labels) and one for their values.'
			},
			pie3D: {
				title: '3D 饼图',
				urlImg: 'https://cloud.highcharts.com/images/erifer/3/136.svg',
				config: {
					'chart--type': 'pie',
					'chart-options3d--enabled': true,
					'chart-options3d--alpha': 45,
					'chart-options3d--beta': 0,
					'plotOptions-pie--allowPointSelect': true,
					'plotOptions-pie--depth': 35,
					'plotOptions-pie--cursor': 'pointer',
					'plotOptions-series-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires two data columns: one for slice names (shown in data labels) and one for their values.'
			},
			pielegend: {
				title: '包含图例',
				urlImg: 'https://cloud.highcharts.com/images/anofof/0/136.svg',
				config: {
					'chart--type': 'pie',
					'plotOptions-pie--allowPointSelect': true,
					'plotOptions-pie--cursor': true,
					'plotOptions-pie--showInLegend': true,
					'plotOptions-pie-dataLabels--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Requires two data columns: one for slice names (shown in the legend) and one for their values.'
			},
			pie3Dlegend: {
				title: '3D 饼图、图例',
				urlImg: 'https://cloud.highcharts.com/images/ubopaq/0/136.svg',
				config: {
					'chart--type': 'pie',
					'chart-options3d--enabled': true,
					'chart-options3d--alpha': 45,
					'chart-options3d--beta': 0,
					'plotOptions-pie--allowPointSelect': true,
					'plotOptions-pie--depth': 35,
					'plotOptions-pie--cursor': 'pointer',
					'plotOptions-pie--showInLegend': true,
					'plotOptions-pie-dataLabels--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Requires two data columns: one for slice names (shown in legend) and one for their values.'
			},
			donut: {
				title: '环形图',
				urlImg: 'https://cloud.highcharts.com/images/upaxab/2/136.svg',
				config: {
					'chart--type': 'pie',
					'plotOptions-pie--allowPointSelect': true,
					'plotOptions-pie--cursor': true,
					'plotOptions-pie--innerSize': '60%',
					'plotOptions-pie-dataLabels--enabled': true,
					'chart--polar': false
				},
				tooltipText: 'Requires two data columns: one for slice names (shown in data labels) and one for their values.'
			},
			donutlegend: {
				title: '环形图，图例',
				urlImg: 'https://cloud.highcharts.com/images/arutag/1/136.svg',
				config: {
					'chart--type': 'pie',
					'plotOptions-pie--allowPointSelect': true,
					'plotOptions-pie--cursor': true,
					'plotOptions-pie--showInLegend': true,
					'plotOptions-pie--innerSize': '60%',
					'plotOptions-pie-dataLabels--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Donut with categories. Requires two data columns: one for slice names (shown in legend) and one for their values.'
			},
			donut3D: {
				title: '3D 环形图',
				urlImg: 'https://cloud.highcharts.com/images/ehuvoh/3/136.svg',
				config: {
					'chart--type': 'pie',
					'chart-options3d--enabled': true,
					'chart-options3d--alpha': 45,
					'chart-options3d--beta': 0,
					'plotOptions-pie--allowPointSelect': true,
					'plotOptions-pie--depth': 35,
					'plotOptions-pie--cursor': 'pointer',
					'plotOptions-series-dataLabels--enabled': true,
					'plotOptions-pie--innerSize': '60%',
					'chart--polar': false
				},
				tooltipText: 'Requires two data columns: one for slice names (shown in data labels) and one for their values.'
			},
			donut3Dlegend: {
				title: '3D 环形图，图例',
				urlImg: 'https://cloud.highcharts.com/images/oriwyb/1/136.svg',
				config: {
					'chart--type': 'pie',
					'chart-options3d--enabled': true,
					'chart-options3d--alpha': 45,
					'chart-options3d--beta': 0,
					'plotOptions-pie--allowPointSelect': true,
					'plotOptions-pie--depth': 35,
					'plotOptions-pie--cursor': 'pointer',
					'plotOptions-series-dataLabels--enabled': false,
					'plotOptions-pie--showInLegend': true,
					'plotOptions-pie--innerSize': '60%',
					'chart--polar': false
				},
				tooltipText: '3D Donut with categories. Requires two data columns: one for slice names (shown in data labels) and one for their values.'
			},
			semicircledonut: {
				title: '扇形图',
				urlImg: 'https://cloud.highcharts.com/images/iwyfes/2/136.svg',
				config: {
					'chart--type': 'pie',
					'plotOptions-pie--allowPointSelect': false,
					'plotOptions-series-dataLabels--enabled': true,
					'plotOptions-pie-dataLabels--distance': -30,
					'plotOptions-pie-dataLabels--style': {
						fontWeight: 'bold',
						color: 'white',
						textShadow: '0px 1px 2px black'
					},
					'plotOptions-pie--innerSize': '50%',
					'plotOptions-pie--startAngle': -90,
					'plotOptions-pie--endAngle': 90,
					'plotOptions-pie--center': ['50%', '75%'],
					'chart--polar': false
				},
				tooltipText: 'Requires two data columns: one for slice names (shown in data labels) and one for their values.'
			}
		}
	},
	polar: {
		title: '极地图',
		templates: {
			polarLine: {
				title: '极地图',
				urlImg: 'https://cloud.highcharts.com/images/ajogud/2/136.svg',
				config: {
					'chart--type': 'line',
					'chart--polar': true
				},
				tooltipText: 'Requires one column for X values or categories (labels around the perimeter), subsequently one column for each series\' Y values ' +
				'(plotted from center and out).'
			},
			spiderLine: {
				title: '蜘蛛图',
				urlImg: 'https://cloud.highcharts.com/images/uqonaj/0/136.svg',
				config: {
					'chart--type': 'line',
					'chart--polar': true,
					'xAxis--tickmarkPlacement': 'on',
					'xAxis--lineWidth': 0,
					'yAxis--lineWidth': 0,
					'yAxis--gridLineInterpolation': 'polygon'
				},
				tooltipText: 'Requires one column for X values or categories (labels around the perimeter), subsequently one column for each series\' Y values ' +
				'(plotted from center and out).'
			},
			polarArea: {
				title: '极地面积图',
				urlImg: 'https://cloud.highcharts.com/images/oqajux/0/136.svg',
				config: {
					'chart--type': 'area',
					'chart--polar': true
				},
				tooltipText: 'Requires one column for X values or categories (labels around the perimeter), subsequently one column for each series\' Y values ' +
				'(plotted from center and out).'
			},
			spiderArea: {
				title: '蜘蛛面积图',
				urlImg: 'https://cloud.highcharts.com/images/exajib/0/136.svg',
				config: {
					'chart--type': 'area',
					'chart--polar': true,
					'xAxis--tickmarkPlacement': 'on',
					'xAxis--lineWidth': 0,
					'yAxis--lineWidth': 0,
					'yAxis--gridLineInterpolation': 'polygon'
				},
				tooltipText: 'Requires one column for X values or categories (labels around the perimeter), subsequently one column for each series\' Y values ' +
				'(plotted from center and out).'
			}
		}
	},
	stock: {
		title: '股票图',
		templates: {
			basic: {
				title: '基础股票图',
				urlImg: 'https://cloud.highcharts.com/images/awuhad/3/136.svg',
				constr: 'StockChart',
				config: {
					'chart--type': 'line',
					'rangeSelector--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			areastock: {
				title: '面积图',
				urlImg: 'https://cloud.highcharts.com/images/ukaqor/136.svg',
				constr: 'StockChart',
				config: {
					'chart--type': 'area',
					'rangeSelector--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			columnstock: {
				title: '柱形图',
				urlImg: 'https://cloud.highcharts.com/images/ogywen/136.svg',
				constr: 'StockChart',
				config: {
					'chart--type': 'column',
					'rangeSelector--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.'
			},
			ohlc: {
				title: 'OHLC K线图',
				urlImg: 'https://cloud.highcharts.com/images/opilip/2/136.svg',
				constr: 'StockChart',
				config: {
					'chart--type': 'ohlc',
					'rangeSelector--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently four columns for each series\' Y values, e.g. open, high, low, close.'
			},
			candlestick: {
				title: '蜡烛图',
				urlImg: 'https://cloud.highcharts.com/images/etybef/0/136.svg',
				constr: 'StockChart',
				config: {
					'chart--type': 'candlestick',
					'rangeSelector--enabled': false,
					'chart--polar': false
				},
				tooltipText: 'Requires one column for X values or categories, subsequently four columns for each series\' Y values, e.g. open, high, low, close.'
			}
		}
	},
	more: {
		title: '更多图表类型',
		templates: {
			solidgauge: {
				title: '仪表图',
				urlImg: 'https://cloud.highcharts.com/images/apocob/0/136.svg',
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.',
				config: {
					'chart--type': 'solidgauge',
					'pane--center': ['50%', '85%'],
					'pane--size': '140%',
					'pane--startAngle': '-90',
					'pane--endAngle': '90',
					'pane--background': {
						backgroundColor: '#EEE',
						innerRadius: '60%',
						outerRadius: '100%',
						shape: 'arc'
					},
					'tooltip--enabled': false,
					'yAxis--stops': [
						[0.1, '#55BF3B'], // green
						[0.5, '#DDDF0D'], // yellow
						[0.9, '#DF5353'] // red
					],
					'yAxis--min': 0,
					'yAxis--max': 100,
					'yAxis--lineWidth': 0,
					'yAxis--minorTickInterval': null,
					'yAxis--tickPixelInterval': 400,
					'yAxis--tickWidth': 0,
					'yAxis-title--y': -70,
					'yAxis-labels--y': 16,
					'plotOptions-solidgauge-dataLabels--y': 10,
					'plotOptions-solidgauge-dataLabels--borderWidth': 0,
					'plotOptions-solidgauge-dataLabels--useHTML': true,
					'series[0]-dataLabels--format': '<div style="text-align:center"><span style="font-size:25px;color:#000000">{y}</span></div>'
				}
			},
			funnel: {
				title: '漏斗图',
				urlImg: 'https://cloud.highcharts.com/images/exumeq/0/136.svg',
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.',
				config: {
					'chart--type': 'funnel',
					'plotOptions-series-datalabels--color': '#000000',
					'plotOptions-series-dataLabels--softConnector': true,
					'plotOptions-series--neckWidth': '20%',
					'plotOptions-series--neckHeight': '35%',
					'series[0]--width': '64%'
				}
			},
			pyramid: {
				title: '金字塔图',
				urlImg: 'https://cloud.highcharts.com/images/obulek/0/136.svg',
				tooltipText: 'Requires one column for X values or categories, subsequently one column for each series\' Y values.',
				config: {
					'chart--type': 'pyramid',
					'plotOptions-series-datalabels--color': '#000000',
					'plotOptions-series-dataLabels--softConnector': true,
					'series[0]--width': '64%'
				}
			},
			boxplot: {
				title: '箱线图',
				urlImg: 'https://cloud.highcharts.com/images/idagib/0/136.svg',
				tooltipText: 'Requires one column for X values, and one column each for low, lower quartile, median, upper quartile and high values.',
				config: {
					'chart--type': 'boxplot'
				}
			}

			// Issue #202 - heatmap makes no sense without proper category support
			//heatmap: {
			//	title: 'Heatmap',
			//	urlImg: 'https://cloud.highcharts.com/images/NOTREADY/0/136.svg',
			//	tooltipText: 'Requires ?? TODO',
			//	config: {
			//		'chart--type': 'heatmap',
			//		'plotOptions-series--borderWidth' : 1,
			//		'colorAxis--min' : 0
			//	}
			//},

			//speedometer: {
			//	title: 'Speedometer',
			//	config: {
			//		'chart--type': 'gauge',
			//		'chart--plotBackgroundColor': null,
			//		'chart--plotBackgroundImage': null,
			//		'chart--plotBorderwidth': 0,
			//		'chart-plotShadow': false,
			//		'pane--startAngle': -150,
			//		'pane--endAngle': 150,
			//		'yAxis--min': 0,
			//		'yAxis--max': 200,
			//		'yAxis--minorTickInterval': 'auto',
			//		'yAxis--minorTickWidth': 1,
			//		'yAxis--minorTickLength': 10,
			//		'yAxis--minorTickPosition': 'inside',
			//		'yAxis--minorTickColor': '#666',
			//		'yAxis--tickPixelInterval': 30,
			//		'yAxis--tickWidth': 2,
			//		'yAxis--tickPosition': 'inside',
			//		'yAxis--tickLength': 10,
			//		'yAxis--tickColor': '#666',
			//		'yAxis-labels--step': 2,
			//		'yAxis-labels--rotation': 'auto',
			//		'yAxis-plotBands': [{
			//			from: 0,
			//			to: 120,
			//			color: '#55BF3B' // green
			//		}, {
			//			from: 120,
			//			to: 160,
			//			color: '#DDDF0D' // yellow
			//		}, {
			//			from: 160,
			//			to: 200,
			//			color: '#DF5353' // red
			//		}]
			//	}
			//}
		}
	},
	combinations: {
		title: '混合图',
		templates: {
			lineColumn: {
				title: '直线图，柱状图',
				urlImg: 'https://cloud.highcharts.com/images/ynikoc/0/136.svg',
				config: {
					'chart--type': 'line',
					'series[0]--type': 'column'
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values. By default, the first series is a column series and subsequent series are lines.'
			},
			columnLine: {
				title: '柱状图，直线图',
				urlImg: 'https://cloud.highcharts.com/images/ufafag/0/136.svg',
				config: {
					'chart--type': 'column',
					'series[0]--type': 'line'
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values. By default, the first series is a line series and subsequent series are columns.'
			},
			areaLine: {
				title: '面积图，直线图',
				urlImg: 'https://cloud.highcharts.com/images/ahimym/0/136.svg',
				config: {
					'chart--type': 'line',
					'series[0]--type': 'area'
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values. By default, the first series is a area series and subsequent series are lines.'
			},
			scatterLine: {
				title: '散点图，直线图',
				urlImg: 'https://cloud.highcharts.com/images/etakof/0/136.svg',
				config: {
					'chart--type': 'line',
					'series[0]--type': 'scatter'
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values. By default, the first series is a scatter series and subsequent series are lines.'
			},
			arearangeLine: {
				title: '面积图范围图，直线图',
				urlImg: 'https://cloud.highcharts.com/images/ypepug/0/136.svg',
				config: {
					'chart--type': 'line',
					'series[0]--type': 'arearange'
				},
				tooltipText: 'Requires one data column for X values or categories, subsequently one data column for each series\' Y values. By default, the first series is a arearange series and subsequent series are lines.'
			}
		} // templates-combinations
	}
};

if (typeof module !== 'undefined') {
	module.exports = highed.meta.chartTemplates;
}

