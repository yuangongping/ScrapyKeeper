# -*- coding: utf-8 -*-
from ScrapyKeeper.model import db, Base


class Scheduler(Base):
    __tablename__ = 'scheduler'
    # 爬虫项目id
    project_id = db.Column(db.INTEGER, nullable=False, index=True)
    # 周期调度-月份
    cron_month = db.Column(db.String(255), default="*")
    # 周期调度时间-天, 默认是*
    cron_day_of_month = db.Column(db.String(255), default="*")
    # 周期调度时间-小时, 默认是*
    cron_hour = db.Column(db.String(255), default="*")
    # 周期调度时间-分钟, 默认是0
    cron_minutes = db.Column(db.String(255), default="0")
    # 0/-1  # 是否可以被周期调度 0可以 -1不可以
    enabled = db.Column(db.INTEGER, default=0)
    # periodic/onetime  调度方式 周期性 和 一次性
    run_type = db.Column(db.String(20), default="periodic")
    # 任务描述
    desc = db.Column(db.Text)
    # 任务的参数
    config = db.Column(db.Text)
