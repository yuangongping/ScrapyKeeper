# coding:utf-8
from ScrapyKeeper.model.Scheduler import Scheduler
import redis
import demjson


class RedisSrv(object):
    redis = redis

    @classmethod
    def getRedisUrls(self, args: dict):
        scheduler = Scheduler.query.filter_by(project_id=args.get("project_id")).first()
        storage_management_form = demjson.decode(demjson.decode(scheduler.config).get("storage_management_form"))
        pool = self.redis.ConnectionPool(
            host=storage_management_form.get("redis").get("ip"),
            port=storage_management_form.get("redis").get("port"),
            db=0)
        redis = self.redis.StrictRedis(connection_pool=pool)
        total = redis.scard(args.get("project_name"))
        data = redis.smembers(args.get("project_name"))
        data = list(data)[:20]
        res = ["当前待采集URL队列数量为: {}".format(total)]
        for i in data:
            res.append(str(i))
        return res
