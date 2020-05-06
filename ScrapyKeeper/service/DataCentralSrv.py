import psutil
import datetime
from ScrapyKeeper.service.ProjectSrv import ProjectSrv
from ScrapyKeeper.service.LogManageSrv import LogManageSrv
from ScrapyKeeper.model.Project import db
from ScrapyKeeper.model.DataStorage import DataStorage
from sqlalchemy import func
from ScrapyKeeper.utils.date_tools import get_near_ndays


class DataCentralSrv:
    def get(self):
        cpu_used = self.get_cpu_state()
        memorystate = self.getMemorystate()
        projectSrv = ProjectSrv()
        projectSrv.update_all_spider_running_status()
        project_running_status = projectSrv.statistical_running_status()
        log_errors = LogManageSrv.log_count()
        log_status = {
            "normal": 0,
            "error": 0
        }
        for log in log_errors:
            if log.get("doc_count") > 0:
                log_status["error"] += 1
            else:
                log_status["normal"] += 1
        data = {
            "cupStatus": {
                "used": cpu_used,
                "Unused": 100-cpu_used
            },
            "memorystate": {
                "used": memorystate.get("used"),
                "Unused": memorystate.get("total") - memorystate.get("used")
            },
            "project_running_status": {
                "waitting": project_running_status.get("waitting"),
                "running": project_running_status.get("running")
            },
            "project_error_rate_status": log_status,
            "dataCount": self.get_all_data_count()
        }
        return data

    def get_cpu_state(self, interval=1):
        return psutil.cpu_percent(interval)

    def getMemorystate(self):
        phymem = psutil.virtual_memory()
        return {
            "used": int(phymem.used / 1024 / 1024),
            "total": int(phymem.total / 1024 / 1024)
        }

    def get_all_data_count(self):
        sql = """SELECT TABLE_SCHEMA, TABLE_NAME, (TABLE_ROWS) FROM
                    information_schema.TABLES
                    WHERE TABLE_SCHEMA = 'duocaiyunspdier';"""
        all = db.engine.execute(sql)
        count = 0
        for item in all:
            count += item[2]
        return count

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
        projects = DataStorage.query.with_entities(DataStorage.project_alias).group_by(DataStorage.project_name).order_by(DataStorage.date_created.desc()).all()
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
                                DataStorage.project_alias == project.replace("\n", '')
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





