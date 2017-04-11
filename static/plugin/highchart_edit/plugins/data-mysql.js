/*

Highcharts Editor v0.1.1

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

*/
highed.plugins.import.install("Mysql",{description:"Mysql is an open data format commonly used for various mysql tables. ",treatAs:"csv",fetchAs:"json",defaultURL:"http://search.hillinsight.com:6688/mysql?online=1&db=hillinsight&table=qingbaotong_cata_data",options:{includeFields:{type:"string",label:"Fields to include, separate by whitespace",default:"month sale_num"}},filter:function(i,e,n){var t=[],s=[];e.includeFields=highed.arrToObj(e.includeFields.split(" ")),highed.isArr(i)&&(i=i.map(function(i){var n={};return Object.keys(e.includeFields).forEach(function(e){n[e]=i[e]}),n}),i.forEach(function(i,n){var l=[];Object.keys(i).forEach(function(t){var a=i[t];e.includeFields[t]&&(0==n&&s.push(t),l.push(parseInt(a)||a))}),t.push(l.join(","))})),n(!1,[s.join(",")].concat(t).join("\n"))}});