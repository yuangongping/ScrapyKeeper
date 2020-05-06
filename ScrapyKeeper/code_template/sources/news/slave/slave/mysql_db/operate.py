# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DB_CONFIG
from .tables import Base


config = DB_CONFIG
engine_words = '{}://{}:{}@{}:{}/{}?charset={}'.format(
    config.get('dbtype'),
    config.get('username'),
    config.get('password'),
    config.get('host'),
    config.get('port'),
    config.get('dbname'),
    config.get('charset')
)
engine = create_engine(engine_words)
# 绑定引擎
Session = sessionmaker(bind=engine)
# 生成session
session = Session()
# 自动建表
Base.metadata.create_all(engine)
