# -*- coding: utf-8 -*-
from ScrapyKeeper.model import db, Base


class DataStorage(Base):
    __tablename__ = 'datastorage'
    project_id = db.Column(db.String(100))
    project_name = db.Column(db.String(100))
    project_name_zh = db.Column(db.String(100))
    schudeler_id = db.Column(db.String(100))
    node_ip = db.Column(db.String(100))
    # 存储的批量大小
    num = db.Column(db.Integer, default=50)
    # 存储的附件的大小， 单位为Mb
    file_size = db.Column(db.Integer)
