# coding:utf-8
import redis


class RedisSrv():
    def __init__(self, host, port):
        self.pool = redis.ConnectionPool(host=host, port=port, db=0)
        self.redis = redis.StrictRedis(connection_pool=self.pool)

    def get(self, args: dict):
        total = self.redis.scard(args.get("project_name"))
        data = self.redis.smembers(args.get("project_name"))
        data = list(data)[:20]
        res = ["当前待采集URL队列数量为: {}".format(total)]
        for i in data:
            res.append(str(i))
        return res
