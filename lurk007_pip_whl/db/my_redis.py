import redis

from lurk007_pip_whl.config.conf import redis_conf


class Redis(object):
    @classmethod
    def rd(cls, host=None, port=None, password=None, db=0):
        if host is None:
            host = redis_conf['host']
        if port is None:
            port = redis_conf['port']
        if password is None:
            password = redis_conf['password']
        return redis.Redis(host=host, port=port, decode_responses=True, db=db, password=password)


if __name__ == '__main__':
    rd = Redis.rd()
    rd.flushall()
    name = rd.get("testname")
    print(name)
