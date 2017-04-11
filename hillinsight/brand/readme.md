

从淘宝数据中按照类目把品牌信息拿到，做归一化后灌入品牌库  
  
基本步骤：
1. 从hive中获取类目、品牌、gmv信息  
	`cd data;hive -e "select category2_id, brand, sum(month_sale * view_price) as gmv from ods.tmp where dt='2016-07-01' group by category2_id, brand order by gmv desc > all"`  
2. 将数据分到不同的类目文件中  
    `cat all | python split2files.py`  
3. 一个个文件地灌品牌库  
	`python batch_add2.py -f data/50008825.tsv -F taobao_50008825 > log 2>&1 &`  
4. 查看有冲突的数据，在数据库中进行手工整合  
