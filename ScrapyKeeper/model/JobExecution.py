# -*- coding: utf-8 -*-
from ScrapyKeeper.model import db, Base


class JobExecution(Base):
    __tablename__ = 'job_execution'
    project_id = db.Column(db.INTEGER, nullable=False, index=True)
    scrapyd_job_id = db.Column(db.String(255))
    scheduler_id = db.Column(db.String(255))
    start_time = db.Column(db.String(255))
    end_time = db.Column(db.String(255))
