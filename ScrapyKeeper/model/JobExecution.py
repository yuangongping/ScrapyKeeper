# -*- coding: utf-8 -*-
from ScrapyKeeper.model import db, Base
import datetime


class JobExecution(Base):
    __tablename__ = 'job_execution'
    scheduler_id = db.Column(db.String(255))
    project_id = db.Column(db.INTEGER, nullable=False, index=True)
    scrapyd_url = db.Column(db.String(255))
    node_type = db.Column(db.String(100))
    scrapyd_job_id = db.Column(db.String(255))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    run_type = db.Column(db.String(255))
