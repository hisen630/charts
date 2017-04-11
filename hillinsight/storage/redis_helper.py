#-*- conding: utf-8 -*-

import string, os, sys
import ConfigParser
import redis

class RedisConf(object):

    confDict = ['host', 'port']
    env = os.getenv('HILLINSIGHT_MYSQL_CONF')
    path = '/home/work/conf/storage/redis.conf'
    if env != None and os.path.exists(env.strip()):
        path = env

    def __init__(self, env='dev'):
        conf = ConfigParser.ConfigParser()
        conf.read(self.path)
        confType = env
        if confType in conf.sections():
            for attr in conf.options(confType):
                if attr in self.confDict:
                    setattr(self, attr, conf.get(confType, attr))


class HHRedis(object):
    _redis_client = None

    def __init__(self, env='dev', strict=True, **kwargs):
        conf = RedisConf(env=env)
        self._redis_client = redis.StrictRedis(host=conf.host, port=conf.port, **kwargs) if strict else redis.Redis(host=conf.host, port=conf.port, **kwargs)

    def __getattr__(self, name):
        return getattr(self._redis_client, name)

    def __getitem__(self, name):
        return self._redis_client[name]

    def __setitem__(self, name, value):
        self._redis_client[name] = value

    def __delitem__(self, name):
        del self._redis_client[name]

if __name__ == '__main__':
    r = HHRedis('online')
    print r._redis_client
    print r.set('zx_lalala', '~~~~~~')

    p = HHRedis('online')
    print p._redis_client
    print '~~~~~~~~~~~~~'
    print p.get('zx_lalala')

