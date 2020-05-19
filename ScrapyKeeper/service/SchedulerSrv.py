# -*- coding: utf-8 -*-
from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.Spider import Spider, db
from ScrapyKeeper.model.Project import Project
from ScrapyKeeper.model.Scheduler import Scheduler
from ScrapyKeeper import ram_scheduler
from ScrapyKeeper.model.JobExecution import JobExecution
import demjson
from uuid import uuid1
from ScrapyKeeper.utils.process_settings import get_settings


class SchedulerSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def list_int2str(self, obj):
        temp = ""
        l = len(obj)
        for i in range(l):
            if i < l-1:
                temp += str(i) + ","
            else:
                temp += str(i)
        return temp

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

    def start_up_project(self, project_name: str, project_id: int, scheduler_id=None):
        try:
            job_uuid = uuid1().hex
            # 通过工程找到对应的爬虫实例
            spiders = Spider.query.filter_by(**{"project_id": project_id}).all()
            scheduler = Scheduler.query.filter_by(id=scheduler_id).first()
            scrapyd_job_id = []
            for spider in spiders:
                if spider.type == "master":
                    _project_name = project_name + "_master" 
                    settings = get_settings(scheduler.config, _project_name)
                    # 启动主爬虫
                    master_job_id = self.master_agent.start_spider(
                        spider.project_name,
                        spider.name,
                        job_uuid=job_uuid,
                        scheduler_id=scheduler_id,
                        settings=settings
                    )
                    scrapyd_job_id.append(master_job_id)
                    # 启动成功后， 更新爬虫实例的job_id
                    spider.job_id = master_job_id
                    db.session.commit()
                    dic = {
                        "project_id": project_id,
                        "scrapyd_job_id": master_job_id,
                        "job_uuid": job_uuid,
                        "scrapyd_url": self.master_agent.server_url
                    }
                    JobExecution.save(dic=dic)
                else:
                    for agent in self.slave_agents:
                        _project_name = project_name + "_slave"
                        settings = get_settings(scheduler.config, _project_name)
                        if agent.server_url == spider.address:
                            slave_job_id = agent.start_spider(
                                spider.project_name,
                                spider.name,
                                job_uuid=job_uuid,
                                scheduler_id=scheduler_id,
                                settings=settings
                            )
                            scrapyd_job_id.append(slave_job_id)
                            spider.job_id = slave_job_id
                            db.session.commit()
                            dic = {
                                "project_id": project_id,
                                "scrapyd_job_id": slave_job_id,
                                "job_uuid": job_uuid,
                                "scrapyd_url": agent.server_url
                            }
                            JobExecution.save(dic=dic)
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
            schedular_form = demjson.decode(demjson.decode(args.get("config")).get("schedular_form"))
            run_type = schedular_form.get("type")
            project = Project.query.filter_by(project_name=args.get("project_name")).first()
            # 单次运行
            if run_type == 1:
                dic = {
                    'project_id': project.id,
                    'run_type': "onetime",
                    "desc": "单次执行",
                    "config": args.get("config")
                }
                obj = Scheduler.save(dic=dic)
                self.start_up_project(project_name=project.project_name, 
                                      project_id=project.id, 
                                      scheduler_id=obj.get("id"))
            else:
                cron_month = self.list_int2str(schedular_form.get("schedular").get("cron_month"))
                cron_day_of_month = self.list_int2str(schedular_form.get("schedular").get("cron_day_of_month"))
                cron_hour = self.list_int2str(schedular_form.get("schedular").get("cron_hour"))
                cron_minutes = self.list_int2str(schedular_form.get("schedular").get("cron_minutes"))
                dic = {
                    'project_id': project.id,
                    'run_type': "periodic",
                    'cron_month': cron_month,
                    'cron_day_of_month': cron_day_of_month,
                    'cron_hour': cron_hour,
                    'cron_minutes': cron_minutes,
                    "desc": schedular_form.get("schedular").get("description"),
                    "config": args.get("config")
                }

                obj = Scheduler.save(dic=dic)
                ram_scheduler.add_job(
                    self.start_up_project,
                    kwargs={"args": {"project_name": project.project_name,
                                     "id": project.id, "scheduler_id": obj.get("id")}
                            },
                    trigger='cron',
                    id=obj.get("id"),
                    month='{}'.format(cron_month),
                    day='{}'.format(cron_day_of_month),
                    hour='{}'.format(cron_hour),
                    minute='{}'.format(cron_minutes),
                    second=0,
                    max_instances=5000,
                    misfire_grace_time=60 * 60,
                    coalesce=True
                )
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
        
    def getbyid(self, id=None):
        return Scheduler.query.filter_by(id=id).first().to_dict()

