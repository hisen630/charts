import os

_mysql_config = {}

def load_mysql_config():
    env = os.getenv('HILLINSIGHT_MYSQL_CONF')
    conf_filename = '/home/work/conf/storage/mysql.conf'
    if env != None and os.path.exists(env.strip()):
        conf_filename = env
    configs = {}
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
        db_key = config["db"] + ("_online" if config["online"] == "1" else "_offline")
        if db_key not in configs:
            configs[db_key] = {"master": None, "slave": []}
        if config["master"] == "1":
            configs[db_key]["master"] = config
        else:
            configs[db_key]["slave"].append(config)
    return configs
_mysql_config = load_mysql_config()
# if __name__ == "__main__":
#     print load_mysql_config()
