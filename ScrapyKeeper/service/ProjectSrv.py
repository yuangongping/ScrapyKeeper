#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProjectSrv.py
# @Time    : 2020-4-29 18:03
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import os
import tempfile
import time
from werkzeug.utils import secure_filename
from xpinyin import Pinyin
from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.Project import Project
from ScrapyKeeper.model.Scheduler import Scheduler
from ScrapyKeeper.model.Spider import Spider, db
from ScrapyKeeper.code_template.ScrapyGenerator import ScrapyGenerator
from ScrapyKeeper.utils.ThreadWithResult import ThreadWithResult
from ScrapyKeeper.service.LogManageSrv import LogManageSrv
from sqlalchemy import and_
import shutil


class DistributeRes(object):
    def __init__(self):
        self._master = None
        self._slaves = []

    def set_master(self, val):
        self._master = val

    def push_slaves(self, val):
        self._slaves.append(val)

    @property
    def master(self):
        return self._master

    @property
    def slaves(self):
        return self._slaves


class ProjectSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def distribute_in_multi_thread(self, func: str, master_args: tuple, slave_args: tuple) -> "DistributeRes":
        """ 分布式部署的情况下，用多线程的方式在主从中运行相同的函数 """
        master_thread = ThreadWithResult(target=getattr(self.master_agent, func), args=master_args)
        master_thread.start()

        slave_threads = []
        for agent in self.slave_agents:
            t = ThreadWithResult(target=getattr(agent, func), args=slave_args)
            slave_threads.append(t)
            t.start()

        master_thread.join()
        [t.join() for t in slave_threads]

        distri_res = DistributeRes()
        distri_res.set_master(master_thread.get_result())
        for t in slave_threads:
            try:
                result = t.get_result()
                distri_res.push_slaves(result)
            except Exception as e:
                print(e)
        return distri_res

    def gen_name(self, name_zh: str) -> str:
        pinyin = Pinyin()
        name_en = pinyin.get_pinyin(name_zh)
        name = ''.join(name_en.split("-"))

        # TODO: 前端通过中文生成项目英文名并提交，存在相同英文名的时候，提醒用户自己手动修改英文名
        exist = Project.find_by_name(name)
        if exist:
            abort(400, message="存在相同的工程名称，请重新命名")
        else:
            return name

    def add_project_by_template(self, tpl_name: str, tpl_args: dict):
        tpl_args['project_name'] = self.gen_name(tpl_args['project_name_zh'])
        egg_path = ScrapyGenerator.gen(tpl_name, **tpl_args)
        if egg_path.get('master') is not None:
            # 分布式
            if egg_path.get('slave') is not None:
                project = {"is_msd": 1}
                project.update(tpl_args)
            # 单机
            else:
                project = {"is_msd": 0}
                project.update(tpl_args)
            deploy_status = self.deploy(
                project=project,
                egg_path_master=egg_path.get("master"),
                egg_path_slave=egg_path.get("slave")
            )

            if deploy_status:
                proj_db = Project.save({
                    "is_msd": 1,
                    "category": tpl_args["category"],
                    "project_name": tpl_args['project_name'],
                    "project_name_zh": tpl_args['project_name_zh'],
                    "tpl_input": tpl_args.get("tpl_input")})
                self.sync_spiders(tpl_args['project_name'])
                return proj_db
            abort(500, message="部署失败")
        abort(500, message="生成工程失败")

    def add_project(self, project_name_zh: str, master_egg, slave_egg=None):
        name_en = self.gen_name(project_name_zh)
        master_filename = secure_filename(master_egg.filename)  # 获取master文件名
        slave_filename = secure_filename(slave_egg.filename)  # 获取slave文件名

        dst_master_egg = os.path.join(tempfile.gettempdir(), master_filename)  # 拼接文件路径
        dst_slave_egg = os.path.join(tempfile.gettempdir(), slave_filename)  # 拼接文件路径

        slave_egg.save(dst_slave_egg)  # 保存slave文件
        master_egg.save(dst_master_egg)  # 保存master文件

        proj = {
                'is_msd': 1,
                'project_name': name_en,
                'project_name_zh': project_name_zh
            }

        deploy_status = self.deploy(
            project=proj,
            egg_path_master=dst_master_egg,
            egg_path_slave=dst_slave_egg
        )

        if deploy_status:
            proj_db = Project.save(proj)
            self.sync_spiders(name_en)
            return proj_db
        abort(500, message="部署失败")

    def edit_project(self, **kwargs):
        return Project.save(dic=kwargs)

    def list_projects(self, args: dict):
        exp_list = []
        if args.get("project_name_zh"):
            words = args.get("project_name_zh").split(' ')
            for word in words:
                exp_list.append(Project.project_name_zh.like('%{}%'.format(word)))
        if args.get("status"):
            exp_list.append(Project.status == args.get("status"))
        if args.get("category"):
            exp_list.append(Project.category == args.get("category"))
        if args.get("project_name"):
            exp_list.append(Project.project_name == args.get("project_name"))
        order_exp = Project.date_created.desc()
        if len(exp_list) > 0:
            filter_exp = and_(*exp_list)
            pagination = Project.query.filter(filter_exp).order_by(order_exp).paginate(
                args.get("page_index"), args.get("page_szie"), error_out=False)
        else:
            pagination = Project.query.order_by(order_exp).paginate(args.get("page_index"), args.get("page_size"), error_out=False)

        projects = pagination.items
        self.update_spider_status(projects)

        data = []
        for project in projects:
            proj = project.to_dict()
            proj["error"] = 0
            data.append(proj)

        return {"total": pagination.total, "data": data}

        # log_error_list = LogManageSrv.log_count()
        # data = []
        # for project in projects:
        #     proj = project.to_dict()
        #     scheduler = Scheduler.query.filter_by(project_id=project.id).first()
        #     proj["error"] = 0
        #     proj["time"] = scheduler.desc if scheduler else "待添加调度"
        #     if log_error_list:
        #         for log_err in log_error_list:
        #             if proj["project_name"] in log_err["key"]:
        #                 proj["error"] = log_err["doc_count"]
        #                 break
        #     data.append(proj)
        #
        # return {"total": pagination.total, "data": data}

    def del_projects(self, **kwargs):
        # 删除srcapyd主服务器的指定工程下的所有版本
        res = self.distribute_in_multi_thread(func='del_project',
                                              master_args=(kwargs['project_name'],),
                                              slave_args=(kwargs['project_name'],))

        if not res.master:
            abort(500, message="删除主节点时出现错误！")

        if not all(res.slaves):
            abort(500, message="删除从节点时出现错误！")

        # 删除系统上的数据库
        Project.delete(filters={"id": kwargs['id']})
        Spider.delete(filters={"project_id": kwargs['id']})
        Scheduler.delete(filters={"project_id": kwargs['id']})
        path = os.path.dirname(os.path.dirname(__file__)) + '/code_template/target/'
        # shutil.rmtree()
        return "已删除工程！"

    def deploy(self, project: dict, egg_path_master: str, egg_path_slave: str = None) -> bool:
        # TODO dict 参数的代码优化
        if egg_path_slave is not None and project['is_msd'] == 1:
            version = int(time.time())

            res = self.distribute_in_multi_thread(func='deploy',
                                                  master_args=(project['project_name'], version, egg_path_master),
                                                  slave_args=(project['project_name'], version, egg_path_slave))

            return res.master and any(res.slaves)

    def sync_spiders(self, project_name: str):
        # 获取工程id
        project = Project.find_by_name(project_name)
        # 获取工程下的蜘蛛列表, 然后更新至数据库
        res = self.distribute_in_multi_thread(func='list_spiders_and_addr',
                                              master_args=(project_name,),
                                              slave_args=(project_name,))

        master_spider_name = res.master['spider_list'][0]
        # 更新数据库
        Spider.save({
            "name": master_spider_name,
            "project_id": project.id,
            "project_name": project.project_name,
            "type": "master",
            "address": self.master_agent.server_url
        })

        for slave in res.slaves:
            Spider.save({
                "name": slave['spider_list'][0],
                "project_id": project.id,
                "project_name": project.project_name,
                "type": "slave",
                "address": slave['address']
            })

    def update_spider_status(self, projects: list("Project")):
        for project in projects:
            spiders = Spider.query.filter_by(type="slave", project_id=project.id).all()

            status = None
            for spider in spiders:
                for slave_agent in self.slave_agents:
                    if slave_agent.server_url == spider.address:
                        status = slave_agent.job_status(
                            spider.project_name,
                            spider.job_id
                        )
                        break
                if status:
                    break
            project.status = status
            db.session.commit()

    def statistical_running_status(self):
        total = Project.query.all()
        running = Project.query.filter_by(status="running").all()
        return {
            "waitting": len(total) - len(running),
            "running": len(running)
        }



