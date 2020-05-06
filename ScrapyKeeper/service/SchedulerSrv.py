# -*- coding: utf-8 -*-
from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.Spider import Spider, db
from ScrapyKeeper.model.Project import Project
from ScrapyKeeper.model.Scheduler import Scheduler
from ScrapyKeeper import ram_scheduler


class SchedulerSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def add_existed_job_to_ram_scheduler(self):
        schedulers = Scheduler.query.all()
        for scheduler in schedulers:
            ram_scheduler.add_job(
                self.start_up_project,
                kwargs={"args": {"project_id": scheduler.project_id}},
                trigger='cron',
                id=scheduler.project_id,
                month='{}'.format(scheduler.cron_month),
                day='{}'.format(scheduler.cron_day_of_month),
                hour='{}'.format(scheduler.cron_hour),
                minute='{}'.format(scheduler.cron_minutes),
                second=0,
                max_instances=5000,
                misfire_grace_time=60 * 60,
                coalesce=True
            )

    def start_up_project(self, args: dict):
        try:
            # 通过工程找到对应的爬虫实例
            filters = {"project_id": args.get("id")}
            spiders = Spider.query.filter_by(**filters).all()
            for spider in spiders:
                if spider.type == "master":
                    # 启动主爬虫
                    master_job_id = self.master_agent.start_spider(
                        spider.project_name,
                        spider.name
                    )
                    # 启动成功后， 更新爬虫实例的job_id
                    spider.job_id = master_job_id
                    db.session.commit()
                else:
                    for agent in self.slave_agents:
                        if agent.server_url == spider.address:
                            slave_job_id = agent.start_spider(
                                spider.project_name,
                                spider.name
                            )
                            spider.job_id = slave_job_id
                            db.session.commit()
            return True
        except:
            return None

    def cancel_running_project(self,  args: dict):
        try:
            # 通过工程找到对应的爬虫实例
            filters = {"project_id": args.get("id")}
            spiders = Spider.query.filter_by(**filters).all()
            for spider in spiders:
                if spider.type == "master":
                    # 启动主爬虫
                    master_job_id = self.master_agent.cancel_spider(
                        spider.project_name,
                        spider.job_id
                    )
                    # 启动成功后， 更新爬虫实例的job_id
                    project = Project.query.filter_by(id=args.get("id")).first()
                    project.status = "休眠"
                    db.session.commit()
                else:
                    for agent in self.slave_agents:
                        if agent.server_url == spider.address:
                            slave_job_id = agent.cancel_spider(
                                spider.project_name,
                                spider.job_id
                            )
                            # 启动成功后， 更新爬虫实例的job_id
                            project = Project.query.filter_by(id=args.get("id")).first()
                            project.status = "休眠"
                            db.session.commit()
            return True
        except:
            return None

    def add_scheduler(self, args: dict):
        try:
            ram_scheduler.add_job(
                self.start_up_project,
                kwargs={"args": {"project_id": args.get("project_id")}},
                trigger='cron',
                id=args.get("project_id"),
                month='{}'.format(args.get("cron_month")),
                day='{}'.format(args.get("cron_day_of_month")),
                hour='{}'.format(args.get("cron_hour")),
                minute='{}'.format(args.get("cron_minutes")),
                second=0,
                max_instances=5000,
                misfire_grace_time=60 * 60,
                coalesce=True
            )
            Scheduler.save(dic=args)
            return True
        except:
            return False

    def cancel_scheduler(self, args: dict):
        try:
            ram_scheduler.remove_job(args.get("project_id"))
            Scheduler.delete(filters={"project_id": args.get("project_id")})
            return True
        except:
            return None
