# coding:utf-8
from __base__ import RTC
from common.mysql_base import check_conf, parse_mysql
from hillinsight.storage.dbs import create_engine_custom

""" sum(gmv)  关键字 sql聚合 """


class Manager(RTC):
    type = 0  # 类型为mysql

    def preview(self, row, oper):
        database_config = row["dbs"]
        _r = check_conf(database_config)
        if _r.get("status", 1) == 0:
            return _r
        conf = parse_mysql(database_config)
        conn = create_engine_custom(dbn=conf['ENGINE'], db=conf['NAME'], host=conf['HOST'], port=conf['PORT'],
                                    user=conf['USER'], pw=conf['PASSWORD'])

        for item in conn.query("show tables;"):
            print item
            # 没有关闭数据库连接吗？conn.close()
