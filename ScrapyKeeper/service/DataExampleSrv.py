#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_restful import abort
from sqlalchemy import DateTime, Date, Numeric


class DataExampleSrv(object):
    @classmethod
    def to_dict(cls, data):
        dic = {}
        for column in data.__table__.columns:
            value = getattr(data, column.name)
            if not value:
                value = None
            elif isinstance(column.type, Date):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(column.type, DateTime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(column.type, Numeric):
                value = float(value)
            dic[column.name] = value
        return dic

    @classmethod
    def data_example(cls, args: dict):

        # try:
            mysql_url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
                args.get('username'),
                args.get('password'),
                args.get('host'),
                args.get('port'),
                args.get('dbname')
            )
            engine = create_engine(mysql_url)
            mysql_base = automap_base()  # 自动创建类
            mysql_base.prepare(engine, reflect=True)
            Session = sessionmaker(bind=engine)  # 绑定引擎
            session = Session()  # 生成session
            table_name = mysql_base.classes[args.get('project_name')]
            data_query = session.query(table_name).limit(10)
            data_example = []
            for data in data_query:
                data_example.append(cls.to_dict(data))
            return data_example
        #
        # except Exception as e:
        #     abort(500, message='data example query failed')

