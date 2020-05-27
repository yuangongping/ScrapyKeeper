#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_restful import abort
from sqlalchemy import DateTime, Date, Numeric
import demjson
from ScrapyKeeper.model.Scheduler import Scheduler


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
        # TODO: 1增加多种数据库支持；2、获取数据库大小写敏感设置再去获取表名 3、给一个反序id
        try:
            scheduler = Scheduler.query.filter_by(project_id=args.get("project_id")).first()
            if scheduler is None:
                return []
            storage_management_form = demjson.decode(demjson.decode(scheduler.config).get("storage_management_form"))
            usrename = storage_management_form.get("storage_content").get("username", 'root')
            password = storage_management_form.get("storage_content").get("password", 'root')
            host = storage_management_form.get("storage_content").get("ip", '10.5.9.110')
            port = storage_management_form.get("storage_content").get("port", 3306)
            db_name = storage_management_form.get("storage_content").get("dbname", 'duocaiyuanspider_dataresource')
            mysql_url = 'mysql+pymysql://{}:{}@{}:{}/{}' .format(usrename, password, host, port, db_name)
            print('DataExample Sql Words  %s  Table %s ' % (mysql_url, args['project_name']))
            engine = create_engine(mysql_url)
            mysql_base = automap_base()  # 自动创建类
            mysql_base.prepare(engine, reflect=True)
            Session = sessionmaker(bind=engine)  # 绑定引擎
            session = Session()  # 生成session
            table_orm = mysql_base.classes[args['project_name'].lower()]
            data_query = session.query(table_orm).order_by(table_orm.id.desc()).limit(20)
            data_example = []
            for data in data_query:
                data_example.append(cls.to_dict(data))
            return data_example
        except Exception as e:
            abort(500, message='data example query failed')
        finally:
            if session:
                session.close()
