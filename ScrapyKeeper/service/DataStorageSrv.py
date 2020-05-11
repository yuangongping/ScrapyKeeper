# -*- coding: utf-8 -*-
from ScrapyKeeper.model.DataStorage import DataStorage, db
from sqlalchemy import func


class DataStorageSrv:
    def add(self, args: dict):
        return DataStorage.save(args)

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
