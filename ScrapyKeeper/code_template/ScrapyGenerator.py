# -*- coding: utf-8 -*-
import os
import importlib
from ScrapyKeeper.utils.ThreadWithResult import ThreadWithResult


class ScrapyGenerator(object):
    @classmethod
    def create_scrapy_project(cls, template: str, **kwargs):
        module_import_words = 'ScrapyKeeper.code_template.sources.%s.generator' % template
        tmpl_gen_module = importlib.import_module(module_import_words)
        tmpl_gen_module.generate(**kwargs)

    @classmethod
    def exec_egg_cli(cls, root_path: str, template: str, project_name: str, m_or_s: str) -> str:
        """ 执行生成egg文件的cli """
        # TODO scrapyd-deploy有很多功能，打包成egg只是其中的一个功能，考虑将其抽离出来
        project_with_suffix = project_name + "_{}".format(m_or_s)

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
        # TODO 考虑单机爬虫
        try:
            root_path = os.path.dirname(os.path.dirname(__file__))
            task_m = ThreadWithResult(target=cls.exec_egg_cli, args=(
                root_path, template, project_name, 'master'
            ))
            task_s = ThreadWithResult(target=cls.exec_egg_cli, args=(
                root_path, template, project_name, 'slave'
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
    def gen(cls, template: str, **kwargs) -> dict:
        cls.create_scrapy_project(template=template, **kwargs)
        return cls.create_egg(template=template, project_name=kwargs['project_name'])




