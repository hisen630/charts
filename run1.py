# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/demo')
def index():
    menus = {
        "menus": [
            {
                "sort": 90,
                "status": 1,
                "name": "任务管理",
                "parent_id": 0,
                "level": 1,
                "url": "/task/",
                "child": [
                    {
                        "sort": 100,
                        "status": 1,
                        "name": "任务查看",
                        "parent_id": 10,
                        "level": 2,
                        "url": "/task/index",
                        "child": [],
                        "id": 11
                    },
                    {
                        "sort": 100,
                        "status": 1,
                        "name": "添加任务",
                        "parent_id": 10,
                        "level": 2,
                        "url": "/task/edit?types",
                        "child": [
                            {
                                "sort": 100,
                                "status": 1,
                                "name": "计算型mysql",
                                "parent_id": 12,
                                "level": 3,
                                "url": "/task/edit?types=1",
                                "child": [],
                                "id": 14
                            },
                            {
                                "sort": 100,
                                "status": 1,
                                "name": "fakecube",
                                "parent_id": 12,
                                "level": 3,
                                "url": "/task/edit?types=2",
                                "child": [],
                                "id": 15
                            },
                            {
                                "sort": 100,
                                "status": 1,
                                "name": "hive",
                                "parent_id": 12,
                                "level": 3,
                                "url": "/task/edit?types=3",
                                "child": [],
                                "id": 21
                            }
                        ],
                        "id": 12
                    },
                    {
                        "sort": 100,
                        "status": 1,
                        "name": "任务日志",
                        "parent_id": 10,
                        "level": 2,
                        "url": "/task/run_index",
                        "child": [],
                        "id": 13
                    }
                ],
                "id": 10
            },
            {
                "sort": 100,
                "status": 1,
                "name": "数据源管理",
                "parent_id": 0,
                "level": 1,
                "url": "/datasource/",
                "child": [
                    {
                        "sort": 100,
                        "status": 1,
                        "name": "查看数据源",
                        "parent_id": 1,
                        "level": 2,
                        "url": "/datasource/index",
                        "child": [],
                        "id": 2
                    },
                    {
                        "sort": 100,
                        "status": 1,
                        "name": "添加数据源",
                        "parent_id": 1,
                        "level": 2,
                        "url": "/datasource/edit?types",
                        "child": [
                            {
                                "sort": 100,
                                "status": 1,
                                "name": "mysql",
                                "parent_id": 3,
                                "level": 3,
                                "url": "/datasource/edit?types=0",
                                "child": [],
                                "id": 4
                            },
                            {
                                "sort": 100,
                                "status": 1,
                                "name": "计算型mysql",
                                "parent_id": 3,
                                "level": 3,
                                "url": "/datasource/edit?types=1",
                                "child": [],
                                "id": 5
                            },
                            {
                                "sort": 100,
                                "status": 1,
                                "name": "fakecube",
                                "parent_id": 3,
                                "level": 3,
                                "url": "/datasource/edit?types=2",
                                "child": [],
                                "id": 6
                            },
                            {
                                "sort": 100,
                                "status": 1,
                                "name": "hive",
                                "parent_id": 3,
                                "level": 3,
                                "url": "/datasource/edit?types=3",
                                "child": [],
                                "id": 20
                            }
                        ],
                        "id": 3
                    }
                ],
                "id": 1
            },
            {
                "sort": 100,
                "status": 1,
                "name": "报表管理",
                "parent_id": 0,
                "level": 1,
                "url": "/chart/",
                "child": [
                    {
                        "sort": 100,
                        "status": 1,
                        "name": "查看报表",
                        "parent_id": 7,
                        "level": 2,
                        "url": "/chart/index",
                        "child": [],
                        "id": 8
                    },
                    {
                        "sort": 100,
                        "status": 1,
                        "name": "添加报表",
                        "parent_id": 7,
                        "level": 2,
                        "url": "/chart/edit",
                        "child": [],
                        "id": 9
                    }
                ],
                "id": 7
            }
        ],
        "bread_crumbs": []
    }
    return render_template("demo.tpl", menus=menus)


if __name__ == '__main__':
	# http://127.0.0.1:16610/demo
    app.debug = True
    app.run(host='0.0.0.0', port=16610, debug=True)
