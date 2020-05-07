import os


def read_file(path):
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content + '\n')


def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def generate(project_name: str, start_url: str, name_zh: str):
    code_root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    template = 'weibo'
    source_tmpl_dir = '{}/{}/{}'.format(code_root_path, 'sources', template)

    dest_proj_dir = '{}/{}/{}/{}'.format(code_root_path, 'target', template, project_name)
    mkdir(dest_proj_dir)
    walk = os.walk(source_tmpl_dir)
    next(walk)  # 第一层目录不做任何事情
    for root, dirs, files in walk:
        for file in files:
            source_file = r'{}/{}'.format(root, file)
            if source_file.endswith(".pyc"):
                continue
            abs_dest_dir = root.replace(source_tmpl_dir, dest_proj_dir)
            abs_dest_dir = abs_dest_dir.replace("master", project_name + "_master").replace("slave", project_name + "_slave")
            mkdir(abs_dest_dir)
            dest_file = '{}/{}'.format(abs_dest_dir, file)

            if "master" in dest_file:
                _project_name = project_name + "_master"
            else:
                _project_name = project_name + "_slave"
            content = read_file(source_file)
            content = content.replace("{{project_name}}", _project_name)
            content = content.replace("__ProjectNamecapitalize__", project_name.capitalize())
            content = content.replace("{{root_project_name}}", project_name)
            content = content.replace("{{project_name_zh}}", name_zh)
            content = content.replace("{{start_url}}", start_url)

            write_file(dest_file, content)


