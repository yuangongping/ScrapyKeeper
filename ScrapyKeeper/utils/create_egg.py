# -*- coding: utf-8 -*-
import threading
import os
from ScrapyKeeper.utils.ThreadWithResult import TreadWithResult

def exec_egg_cli(root_path, template, project_name, is_master):
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


def create_egg(template=None, project_name=None):
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


