# -*- coding: utf-8 -*-
from ScrapyKeeper.model.DataStorage import DataStorage, db
from sqlalchemy import func
import logging
from ScrapyKeeper.model.Scheduler import Scheduler
from ScrapyKeeper.model.Project import Project
from ScrapyKeeper.model.JobExecution import JobExecution
import datetime


class DataStorageSrv:
    def add(self, scheduler_id=None, scrapyd_url=None, num=200, file_size=None):
        scheduler = Scheduler.query.filter_by(id=scheduler_id).first()
        project = Project.query.filter_by(id=scheduler.project_id).first()
        dic = {
            "project_id": project.id,
            "project_name": project.project_name,
            "project_name_zh": project.project_name_zh,
            "schudeler_id": scheduler_id,
            "node_ip": scrapyd_url,
            "num": num,
            'file_size': file_size
        }
        return DataStorage.save(dic)

    def get_project_data_trend(self, args: dict):
        if args.get("project_name_zh"):
            data = db.session.query(
                func.date_format(DataStorage.date_created, '%Y-%m-%d').label('date'),
                func.sum(DataStorage.num)).filter(
                DataStorage.project_name_zh == args.get("project_name_zh")
            ).group_by('date').all()
        else:
            data = db.session.query(
                func.date_format(DataStorage.date_created, '%Y-%m-%d').label('date'),
                func.sum(DataStorage.num)).group_by('date').all()
        return [{"日期": item[0], "入库量": int(item[1])} for item in data]

    def update_start_time(self, scheduler_id=None, scrapyd_url=None):
        job = JobExecution.query.filter_by(
            scheduler_id=scheduler_id,
            scrapyd_url=scrapyd_url
        ).first()
        if job:
            job.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()

    def update_end_time(self, scheduler_id=None, scrapyd_url=None):
        job = JobExecution.query.filter_by(
            scheduler_id=scheduler_id,
            scrapyd_url=scrapyd_url
        ).first()
        if job:
            job.end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()


