======================

Charts

======================

一个根据数据源产生图表的工具.

[Features](#features)  
[Browser Compatibility](#rowser-compatibility)  
[Requirements](#requirements)  
[Use in CommonJS/Node Environments Without `window`](#use-in-commonjsnode-environments-without-window)  
[A Note About Encoding](#a-note-about-encoding)  
[API Reference](#api-reference)

## Features
- Support Mysql、Store Mysql and Hive datasource
- Support highcharts-editor's charts

## Browser Compatibility
The following browsers have passed all of the automated Charts tests:
- Chrome

## Requirements

- Python 2.7
- Conda 4.2.13
- Flask 0.10.1
- Works on Linux
- uwsgi

## Install:

- pip install -r requirements.txt
- run the table_structure.sql in the mysql console
- configure the conf/default's _notebook_path and _notebook_url

- set the path HILLINSIGHT_MYSQL_CONF that the mysql conf like hillinsight/storage/mysql.conf 
    db=database,user=user, pw=password,host=localhost,port=port,master=is_master,online=is_online

## Run:
- run the program
    for run a single thread:
        python run.py
    for run multi-threaded:
        sh start.sh
    for restart the multi-threaded:
        kill -HUP `cat uwsgi.pid`
    for stop the multi-threaded:
        kill -9 `cat uwsgi.pid`
- run the jupyter-notebook


## Recommend crontab like:
- for check and restart notebook
    3 * * * * (ps ux|grep -v grep|grep -qs jupyter-notebook)||(source ~/.bash_profile;cd somewhere/notebook/&&jupyter-notebook >log 2>&1)
- for delete the nouse notebook
    0 4 * * * (ps ux|grep -v grep|grep jupyter-notebook|awk '{print $2}'|xargs kill -9)&&(cd somewhere/notebook/ && rm *.ipynb)
- for check task and add the task to crontab
    * * * * * source ~/.bash_profile && cd somewhere/charts/ && python task_to_auto.py >>auto.log 2>&1