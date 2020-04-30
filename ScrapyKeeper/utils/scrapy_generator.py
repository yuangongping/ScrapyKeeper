# -*- coding: utf-8 -*-
import os
from ScrapyKeeper.code_template.sources.news.generator import MasterFactory, SlaveFactory
from ScrapyKeeper.utils.ThreadWithResult import TreadWithResult


class TemplateGenerator(object):
    @classmethod
    def create_scrapy_project(cls, url=None, name_en=None, name_zh=None, template=None) -> dict:
        url = url
        name_zh = name_zh
        project_name = name_en
        template = template
        factory_master = MasterFactory(
            project_name=project_name, url=url,
            template=template, name_zh=name_zh
        )
        factory_slave = SlaveFactory(
            project_name=project_name, url=url,
            template=template, name_zh=name_zh
        )
        factory_master.creat_all()
        factory_slave.creat_all()

    @classmethod
    def exec_egg_cli(cls, root_path, template, project_name, is_master):
        suffix = 'master' if is_master else 'slave'
        project_with_suffix = project_name + "_{}".format(suffix)

        path = "{}/code_template/target/{}/{}/{}/".format(
            root_path, template, project_name, project_with_suffix
        )

        cmd = "cd {} && scrapyd-deploy -p {} --build-egg={}.egg".format(
            path,
            project_with_suffix,
            project_with_suffix
        )
        # 执行命令
        status = os.system(cmd)
        if status == 0:
            return path + project_with_suffix + '.egg'

    @classmethod
    def create_egg(cls, template=None, project_name=None):
        try:
            root_path = os.path.dirname(os.path.dirname(__file__))
            task_m = TreadWithResult(target=cls.exec_egg_cli, args=(
                root_path, template, project_name, True
            ))
            task_s = TreadWithResult(target=cls.exec_egg_cli, args=(
                root_path, template, project_name, False
            ))
            task_m.start()
            task_s.start()
            task_m.join()
            task_s.join()
            paths = {
                "master": task_m.get_result(),
                "slave": task_s.get_result()
            }
            return paths
        except Exception as e:
            return None

    @classmethod
    def create(cls, url=None, name_en=None, name_zh=None, template=None) -> dict:
        cls.create_scrapy_project(url=url, name_en=name_en, name_zh=name_zh, template=template)
        return cls.create_egg(template=template, project_name=name_en)


