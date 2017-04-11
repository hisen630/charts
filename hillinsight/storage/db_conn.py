from hillinsight.storage import dbs
import os
import pprint
_mysql_config = {}
def load_mysql_config():
    env = os.getenv('HILLINSIGHT_MYSQL_CONF')
    conf_filename = '/home/work/conf/storage/mysql.conf'
    if env != None and os.path.exists(env.strip()):
        conf_filename = env
    dbconns = {}
    configs = []
    for line in open(conf_filename):
        line = line.strip()
        if line.startswith("#") or line == "":
            continue
        fields = line.split(",")
        config = {}
        for field in fields:
            (k,v) = (f.strip() for f in field.split("="))
            if k not in ("db","user","pw","host","port","master","online"):
                continue # ignore invalid key/value pair
            config[k] = v
        configs.append(config)
    for c in configs:
        master_or_slave = ("master" if c["master"] == "1" else "slave")
        m_or_s_bool = (True if c["master"] == "1" else False)
        on_or_offline = ("online" if c["online"] == "1" else "offline")
        on_or_off_bool = (True if c["online"] == "1" else False)
        db = dbs.create_engine(c['db'], master=m_or_s_bool, online=on_or_off_bool)
        if c['db'] not in dbconns:
            dbconns[c['db']] = {'master':{'online':None,'offline':None},'slave':{'online':None,'offline':None}}
        dbconns[c['db']][master_or_slave][on_or_offline] = db
    return dbconns

_mysql_config = load_mysql_config()

if __name__ == '__main__':
    pprint.pprint(_mysql_config)
