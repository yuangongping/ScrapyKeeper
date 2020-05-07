# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DB_CONFIG
from .tables import Post


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


def table_existed(engine, orm):
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    Base.metadata.reflect(engine)
    tables = Base.metadata.tables
    if orm.__tablename__ in tables:
        return True
    else:
        from .tables import Base as ormBase
        ormBase.metadata.create_all(engine)
        return False

firstCrawl = False
if table_existed(engine, Post):
    firstCrawl = True

