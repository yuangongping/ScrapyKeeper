# -*- coding: utf-8 -*-
import uuid

from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.Spider import Spider, db
from ScrapyKeeper.model.Project import Project
from ScrapyKeeper.model.Scheduler import Scheduler
from ScrapyKeeper import ram_scheduler
import demjson

from ScrapyKeeper.service.DataStorageSrv import DataStorageSrv
from ScrapyKeeper.utils.process_settings import get_settings
from ScrapyKeeper.model.JobExecution import JobExecution
import logging
import datetime
import time


class SchedulerSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def format_corn(self, corn_arr):
        arr = [str(corn) for corn in corn_arr]
        return ','.join(arr)

    def add_existed_job_to_ram_scheduler(self):
        schedulers = Scheduler.query.all()
        for scheduler in schedulers:
            # 对单次运行的任务实例不做处理
            if scheduler.run_type != "periodic":
                continue
            project = Project.query.filter_by(id=scheduler.project_id).first()
            args = {
                "project_name": project.project_name,
                "project_id": int(project.id),
                "scheduler_id": scheduler.id,
                "run_type": "periodic",
                "project_name_zh": project.project_name_zh
            }
            ram_job = ram_scheduler.add_job(
                self.start_up_project,
                kwargs=args,
                trigger='cron',
                id=str(scheduler.id),
                month='{}'.format(scheduler.cron_month),
                day='{}'.format(scheduler.cron_day_of_month),
                hour='{}'.format(scheduler.cron_hour),
                minute='{}'.format(scheduler.cron_minutes),
                second=0,
                max_instances=5000,
                misfire_grace_time=60 * 60,
                coalesce=True
            )

    def start_up_project(self, project_name: str, project_id: int, project_name_zh, scheduler_id=None, run_type=None):
        # 通过工程找到对应的爬虫实例
        spiders = Spider.query.filter_by(**{"project_id": project_id}).all()
        scheduler = Scheduler.query.filter_by(id=scheduler_id).first()
        scrapyd_job_id = []

        round_id = uuid.uuid1().hex  # 周期调度的轮次id
        for spider in spiders:
            if spider.type == "master":
                _project_name = project_name + "_master"
                settings = get_settings(scheduler.config,
                                        _project_name,
                                        scheduler_id,
                                        round_id,
                                        project_name,
                                        project_name_zh)
                master_job_id = self.master_agent.start_spider(
                    spider.project_name,
                    spider.name,
                    settings=settings
                )
                print('Master spider %s running in job id %s' % (spider.name, master_job_id))
                if not master_job_id:
                    raise ConnectionError('run master spider %s start job failed !' % spider.name)

                scrapyd_job_id.append(master_job_id)
                # 启动成功后， 更新爬虫实例的job_id
                spider.job_id = master_job_id
                db.session.commit()
                dic = {
                    "project_id": project_id,
                    "scrapyd_job_id": master_job_id,
                    "scheduler_id": scheduler_id,
                    "round_id": round_id,
                    "scrapyd_url": self.master_agent.server_url,
                    "node_type": "master",
                    "run_type": run_type
                }
                JobExecution.save(dic=dic)
            else:
                for agent in self.slave_agents:
                    _project_name = project_name + "_slave"
                    settings = get_settings(scheduler.config,
                                            _project_name,
                                            scheduler_id,
                                            round_id,
                                            project_name,
                                            project_name_zh)
                    if agent.server_url == spider.address:
                        slave_job_id = agent.start_spider(
                            spider.project_name,
                            spider.name,
                            settings=settings
                        )
                        print('Slave spider %s running in job id %s' % (spider.name, slave_job_id))
                        if not slave_job_id:
                            raise ConnectionError('slave spider %s start job failed !' % spider.name)
                        scrapyd_job_id.append(slave_job_id)
                        spider.job_id = slave_job_id
                        db.session.commit()
                        dic = {
                            "project_id": project_id,
                            "scrapyd_job_id": slave_job_id,
                            "scheduler_id": scheduler_id,
                            "round_id": round_id,
                            "scrapyd_url": agent.server_url,
                            "node_type": "slave",
                            "run_type": run_type
                        }
                        JobExecution.save(dic=dic)
        return True

    def cancel_running_project(self,  args: dict):
        try:
            # 通过 调度id 查询所有的任务
            jobs = JobExecution.query.filter_by(scheduler_id=args.get("scheduler_id")).all()
            # 获取该调度所属的工程信息
            porject = Project.query.filter_by(id=jobs[0].project_id).first()
            data_storage = DataStorageSrv()
            # 取消主从节点上的任务
            for job in jobs:
                if job.node_type == "master":
                    master_job_id = self.master_agent.cancel_spider(
                        porject.project_name,
                        job.scrapyd_job_id
                    )
                    # 由于取消爬虫不会关闭爬虫， 故需要手动更新数据库
                    # job.end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print("主爬虫： {} 任务已取消！".format(job.scrapyd_job_id))
                else:
                    for agent in self.slave_agents:
                        if agent.server_url == job.scrapyd_url:
                            slave_job_id = agent.cancel_spider(
                                porject.project_name,
                                job.scrapyd_job_id
                            )
                            # 由于取消爬虫不会关闭爬虫， 故需要手动更新数据库
                            # job.end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print("从爬虫： {} 任务已取消！".format(job.scrapyd_job_id))
                # 更新每个任务的结束时间
                data_storage.update_end_time(
                    scheduler_id=job.scheduler_id,
                    scrapyd_url=job.scrapyd_url,
                    cancel_manually=True
                )
            return True
        except Exception as err:
            abort(500, message=str(err))

    def add_scheduler(self, args: dict):
        try:
            scheduler_form = demjson.decode(demjson.decode(args.get("config")).get("scheduler_form"))
            run_type = scheduler_form.get("type")
            project = Project.query.filter_by(project_name=args.get("project_name")).first()
            # 单次运行
            if run_type == 1:
                dic = {
                    'project_id': project.id,
                    'run_type': "onetime",
                    "desc": "单次执行",
                    "config": args.get("config")
                }
                print("----------------------------------单次运行任务")
                obj = Scheduler.save(dic=dic)
                self.start_up_project(project_name=project.project_name,
                                      project_id=project.id,
                                      scheduler_id=obj.get("id"),
                                      run_type="onetime",
                                      project_name_zh=project.project_name_zh
                                      )
            else:
                cron_month = self.format_corn(scheduler_form.get("scheduler").get("cron_month"))
                cron_day_of_month = self.format_corn(scheduler_form.get("scheduler").get("cron_day_of_month"))
                cron_hour = self.format_corn(scheduler_form.get("scheduler").get("cron_hour"))
                cron_minutes = self.format_corn(scheduler_form.get("scheduler").get("cron_minutes"))
                dic = {
                    'project_id': project.id,
                    'run_type': "periodic",
                    'cron_month': cron_month,
                    'cron_day_of_month': cron_day_of_month,
                    'cron_hour': cron_hour,
                    'cron_minutes': cron_minutes,
                    "desc": scheduler_form.get("scheduler").get("description"),
                    "config": args.get("config")
                }
                obj = Scheduler.save(dic=dic)
                args = {
                        "project_name": project.project_name,
                        "project_id": int(project.id),
                        "scheduler_id": obj.get("id"),
                        "run_type": "periodic",
                        "project_name_zh": project.project_name_zh
                }
                job = ram_scheduler.add_job(
                    self.start_up_project,
                    kwargs=args,
                    trigger='cron',
                    id=str(obj.get("id")),
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
        except Exception as err:
            abort(500, message=str(err))

    def cancel_scheduler(self, args: dict):
        try:
            # 先从scheduler任务调度器中删除该调度任务
            try:
                all_jobs = ram_scheduler.get_jobs()
                for ram_job in all_jobs:
                    if ram_job.id == str(args.get("scheduler_id")):
                        ram_scheduler.remove_job(ram_job.id)
            finally:
                Scheduler.delete(filters={"id": args.get("scheduler_id")})
            return True
        except Exception as err:
            print(err)
            abort(500, message=str(err))
        
    def getbyid(self, id=None):
        return Scheduler.query.filter_by(id=id).first().to_dict()

