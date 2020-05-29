# coding:utf-8
from ScrapyKeeper.model.Scheduler import Scheduler
import redis
import demjson


class RedisSrv(object):
    redis = redis

    @classmethod
    def getRedisUrls(self, args: dict):
        # 通过查询scheduler，用于获取配置参数
        scheduler = Scheduler.query.filter_by(project_id=args.get("project_id")).first()
        # 如果还没有添加调度
        if not scheduler:
            return ["当前待采集URL队列数量为: 0"]
        # 配置参数字符串对象 转 对象
        storage_management_form = demjson.decode(demjson.decode(scheduler.config).get("storage_management_form"))
        # 创建redis的链接
        redis = self.redis.Redis(
            host=storage_management_form.get("redis").get("ip"),
            port=storage_management_form.get("redis").get("port"),
            db=0)
        # 获取待采队列的总数
        total = redis.scard(args.get("project_name"))
        # 从待采队里中随机取20个
        data = redis.srandmember(args.get("project_name"), 20)
        res = ["当前待采集URL队列数量为: {}".format(total)]
        for i in data:
            res.append(str(i))
        return res
