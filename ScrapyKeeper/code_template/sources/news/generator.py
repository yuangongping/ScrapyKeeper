import os


class MasterFactory:
    def __init__(self, project_name=None, url=None, template=None, name_zh=None):
        self.code_root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.template = template
        self.project_name = project_name
        self.start_url = url
        self.name_zh = name_zh

    def __read(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            return f.read()

    def _write(self, path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content + '\n')

    def _makedirs(self, path):
        # 将文件与路径切开
        temp = path.split('/')
        # 获得路径与文件名
        filedirs = '/'.join(temp[:-1])
        # 新建路径, 目录是否存在,不存在则创建
        mkdirlambda = lambda x: os.makedirs(x) if not os.path.exists(x) else True
        mkdirlambda(filedirs)

    def process_scrapycfg(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            'scrapy.cfg'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            'scrapy.cfg'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("$$$$$$$$", self.project_name + "_master")
        self._write(dis_filename, content)

    def process_init(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            '__init__.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_settings(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            'settings.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            'settings.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("$$$$$$$$", self.project_name + "_master")
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Master")
        self._write(dis_filename, content)

    def process_middlewares(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            'middlewares.py'

        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            'middlewares.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Master")
        self._write(dis_filename, content)

    def process_item(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            'items.py'

        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            'items.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Master")
        self._write(dis_filename, content)

    def process_pipelines(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            'pipelines.py'
        ])
        dis_filename= '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            'pipelines.py'

        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Master")
        content = content.replace("$$$$$$$$", self.project_name)
        self._write(dis_filename, content)

    def process_init_next(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            '__init__.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_util_init(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            "utils",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            "utils",
            '__init__.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_util_parse_err(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            "utils",
            'parse_err.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            "utils",
            'parse_err.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_spdiers_init(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            "spiders",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            "spiders",
            '__init__.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_spiders_spider(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "master",
            "master",
            "spiders",
            'master.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_master",
            self.project_name + "_master",
            "spiders",
            self.project_name + '_spider.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Master")
        content = content.replace("$$$$$$$$", self.project_name)
        content = content.replace("&&&&&&&&", self.start_url)
        self._write(dis_filename, content)

    def creat_all(self):
        self.process_scrapycfg()
        self.process_init()
        self.process_settings()
        self.process_middlewares()
        self.process_item()
        self.process_pipelines()
        self.process_init_next()
        self.process_util_init()
        self.process_util_parse_err()
        self.process_spdiers_init()
        self.process_spiders_spider()


class SlaveFactory:
    def __init__(self, project_name=None, url=None, template=None, name_zh=None):
        self.code_root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.template = template
        self.project_name = project_name
        self.start_url = url
        self.name_zh = name_zh

    def __read(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            return f.read()

    def _write(self, path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content + '\n')

    def _makedirs(self, path):
        # 将文件与路径切开
        temp = path.split('/')
        # 获得路径与文件名
        filedirs = '/'.join(temp[:-1])
        # 新建路径, 目录是否存在,不存在则创建
        mkdirlambda = lambda x: os.makedirs(x) if not os.path.exists(x) else True
        mkdirlambda(filedirs)

    def process_scrapycfg(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            'scrapy.cfg'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            'scrapy.cfg'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("$$$$$$$$", self.project_name + "_slave")
        self._write(dis_filename, content)

    def process_init(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            '__init__.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_settings(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            'settings.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            'settings.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("$$$$$$$$", self.project_name + "_slave")
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Slave")
        self._write(dis_filename, content)

    def process_middlewares(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            'middlewares.py'

        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            'middlewares.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Slave")
        self._write(dis_filename, content)

    def process_item(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            'items.py'

        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            'items.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Slave")
        self._write(dis_filename, content)

    def process_pipelines(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            'pipelines.py'
        ])
        dis_filename= '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            'pipelines.py'

        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Slave")
        content = content.replace("$$$$$$$$", self.project_name)
        self._write(dis_filename, content)

    def process_extensions(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            'extensions.py'
        ])
        dis_filename= '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            'extensions.py'

        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_init_next(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            '__init__.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_util_init(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "utils",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "utils",
            '__init__.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_util_extractor(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "utils",
            'extractor.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "utils",
            'extractor.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_util_tools(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "utils",
            'tools.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "utils",
            'tools.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_spdiers_init(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "spiders",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "spiders",
            '__init__.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_spiders_spider(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "spiders",
            'slave.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "spiders",
            self.project_name + '_spider.py'
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("@@@@@@@@", self.project_name.capitalize() + "Master")
        content = content.replace("$$$$$$$$", self.project_name)
        self._write(dis_filename, content)

    def process_mysql_db_init(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "mysql_db",
            '__init__.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "mysql_db",
            "__init__.py"
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_mysql_db_config(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "mysql_db",
            'config.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "mysql_db",
            "config.py"
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_mysql_db_operate(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "mysql_db",
            'operate.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "mysql_db",
            "operate.py"
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        self._write(dis_filename, content)

    def process_mysql_db_tables(self):
        source_filename = '/'.join([
            self.code_root_path,
            "sources",
            self.template,
            "duocaiyun",
            "slave",
            "slave",
            "mysql_db",
            'tables.py'
        ])
        dis_filename = '/'.join([
            self.code_root_path,
            "target",
            self.template,
            self.project_name,
            self.project_name + "_slave",
            self.project_name + "_slave",
            "mysql_db",
            "tables.py"
        ])
        self._makedirs(dis_filename)
        content = self.__read(source_filename)
        content = content.replace("$$$$$$$$", self.project_name)
        content = content.replace("%%%%%%%%", self.name_zh)
        self._write(dis_filename, content)

    def creat_all(self):
        self.process_scrapycfg()
        self.process_init()
        self.process_settings()
        self.process_middlewares()
        self.process_item()
        self.process_pipelines()
        self.process_init_next()
        self.process_util_init()
        self.process_util_extractor()
        self.process_util_tools()
        self.process_spdiers_init()
        self.process_spiders_spider()
        self.process_mysql_db_init()
        self.process_mysql_db_config()
        self.process_mysql_db_operate()
        self.process_mysql_db_tables()
