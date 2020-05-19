# -*- coding: utf-8 -*-
from ScrapyKeeper.model import db, Base


class JobExecution(Base):
    __tablename__ = 'job_execution'
    job_uuid = db.Column(db.String(255))
    project_id = db.Column(db.INTEGER, nullable=False, index=True)
    scrapyd_url = db.Column(db.String(255))
    scrapyd_job_id = db.Column(db.String(255))
    start_time = db.Column(db.String(255))
    end_time = db.Column(db.String(255))
