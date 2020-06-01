from ScrapyKeeper.model.Project import db
from ScrapyKeeper.model.DataStorage import DataStorage
from sqlalchemy import func
from ScrapyKeeper.utils.date_tools import get_near_ndays
from ScrapyKeeper import app


class DataCentralSrv:
    def get(self):
        data = {
            "dataCount": self.get_data_count(),
            "data_size": self.get_data_size() + self.get_file_size(),
            "file_size": self.get_file_size()
        }
        return data
    
    def get_data_info(self):
        sql = """SELECT SUM(num), SUM(file_size) FROM datastorage;"""
        data = db.session.excute()
        return int(data) if data is not None else 0

    def get_data_size(self):
        """
        通过information_schema 表 获取指定库的占用空间大小
        :return:
        """
        name = app.config.get("DATASTORAGENAME")
        sql = """select round(sum(DATA_LENGTH / 1024 ), 2) as data
          from information_schema.TABLES where
          table_schema = '{}';""".format(name)
        all = db.engine.execute(sql)
        data = 0
        for item in all:
            data = int(item[0]) if item[0] else 0
        return data

    def get_week_data(self):
        """
         功能: 统计近7天爬取数据量
         :return: {
            "label_data": ["project_alias1", "project_alias2",  ..., "project_alias7"],
            "xAxis":["05-01", "05-02", ..., "05-07"],
            "yAxis": {
                "05-01": [100, 2000],
                "05-02": [100, 2000],
            }
         }
        """
        N = 50
        # 获取近七天的日期列表
        days = get_near_ndays()
        # 获取数据更新最新的前N个工程名
        try:
            projects = DataStorage.query.with_entities(DataStorage.project_name_zh).group_by(DataStorage.project_name).order_by(DataStorage.date_created.desc()).all()
        except:
            projects = []
        projects = [item[0] if index % 2 == 0 else "\n"+item[0]
                        for index, item in enumerate(projects[:N])]
        # 遍历日期列表， 查询如当天的所有工程的数据总和
        data_num = {}
        for day in days:
            data_num[day] = []
            for project in projects:
                num = DataStorage.query.with_entities(
                                func.sum(DataStorage.num)
                            ).filter(
                                func.date_format(DataStorage.date_created, '%Y-%m-%d') == day,
                                DataStorage.project_name_zh == project.replace("\n", '')
                            ).all()
                if num[0][0]:
                    data_num[day].append(int(num[0][0]))
                else:
                    data_num[day].append(0)
        return {
            "label_data": projects,
            "xAxis": days,
            "yAxis": data_num
        }
