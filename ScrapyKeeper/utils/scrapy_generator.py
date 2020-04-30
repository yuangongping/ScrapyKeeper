import os
import re
from ScrapyKeeper.code_template.sources.news.generator import MasterFactory, SlaveFactory
from xpinyin import Pinyin
from ScrapyKeeper.utils.ThreadWithResult import TreadWithResult


class TemplateGenerator(object):
    @classmethod
    def create_scrapy_project(cls, url, name, template) -> dict:
        name_zh = "人民网"
        url = "https://www.baidu.com/"
        template = "news"

        pinyin = Pinyin()

        project_name = pinyin.get_pinyin(
            re.findall("[\u4e00-\u9fa5]+", name_zh)[0]
        )
        project_name = ''.join(project_name.split("-"))
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
            task_m = TreadWithResult(target=exec_egg_cli, args=(
                root_path, template, project_name, True
            ))
            task_s = TreadWithResult(target=exec_egg_cli, args=(
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
    def create(cls):

