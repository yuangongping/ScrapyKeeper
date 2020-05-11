import os
import json


def read_file(path):
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content + '\n')


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def generate(*args, **kwargs):
    code_root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    template = 'news'
    source_tmpl_dir = '{}/{}/{}'.format(code_root_path, 'sources', template)
    dest_proj_dir = '{}/{}/{}/{}'.format(code_root_path, 'target', template, kwargs['project_name'])
    mkdir(dest_proj_dir)

    walk = os.walk(source_tmpl_dir)
    next(walk)  # 第一层目录不做任何事情
    for root, dirs, files in walk:
        for file in files:
            source_file = r'{}/{}'.format(root, file)
            if source_file.endswith(".pyc"):
                continue
            abs_dest_dir = root.replace(source_tmpl_dir, dest_proj_dir)
            abs_dest_dir = abs_dest_dir.replace("master", kwargs['project_name'] + "_master")\
                .replace("slave", kwargs['project_name'] + "_slave")

            mkdir(abs_dest_dir)
            dest_file = '{}/{}'.format(abs_dest_dir, file)
            content = read_file(source_file)
            if "master" in dest_file:
                _project_name = kwargs['project_name'] + "_master"
            else:
                _project_name = kwargs['project_name'] + "_slave"

            content = content.replace("{{project_name}}", _project_name)
            content = content.replace("__ProjectNamecapitalize__", kwargs['project_name'].capitalize())
            content = content.replace("{{root_project_name}}", kwargs['project_name'])
            content = content.replace("{{project_name_zh}}", kwargs['project_name_zh'])

            write_file(dest_file, content)
