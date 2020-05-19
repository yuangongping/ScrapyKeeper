import demjson


def get_settings(config_str, project_name):
    download_params_form = demjson.decode(demjson.decode(config_str).get("download_params_form"))
    crawl_range_form = demjson.decode(demjson.decode(config_str).get("crawl_range_form"))
    crawl_stratege_form = demjson.decode(demjson.decode(config_str).get("crawl_stratege_form"))
    storage_management_form = demjson.decode(demjson.decode(config_str).get("storage_management_form"))

    settings = {
        "RETRY_ENABLED": True,
        "RETRY_TIMES": download_params_form.get("reapt_num", 1),
        "CONCURRENT_REQUESTS": download_params_form.get("request_num", 8),
        "DOWNLOAD_DELAY": download_params_form.get("download_delay", 0.5),
        "DOWNLOAD_TIMEOUT": download_params_form.get("timeout", 180),
        "DNSCACHE_ENABLED": True,
        "DNSCACHE_SIZE": download_params_form.get("DNS_size", 10000),
        "DNS_TIMEOUT": 60,
        "DEPTH_LIMIT": crawl_range_form.get("level", 0),
        "REDIS_HOST": storage_management_form.get("redis").get("ip", '10.5.9.87'),
        "REDIS_PORT": storage_management_form.get("redis").get("port", 6379),
        "MYSQL_HOST": storage_management_form.get("storage_content").get("ip", '10.5.9.110'),
        "MYSQL_DB": storage_management_form.get("storage_content").get("dbname", 'duocaiyuanspider'),
        "MYSQL_TABLE": storage_management_form.get("storage_content").get("tablename", None),
        "MYSQL_USERNAME": storage_management_form.get("storage_content").get("username", 'root'),
        "MYSQL_PASSWORD": storage_management_form.get("storage_content").get("password", 'root'),
        "MYSQL_PROT": storage_management_form.get("storage_content").get("port", 3306),
    }
    # 如果深度优先
    if crawl_stratege_form.get("stratege", 1) == 1:
        settings["DEPTH_PRIORITY"] = 1
        settings["SCHEDULER_DISK_QUEUE"] = 'scrapy.squeues.PickleFifoDiskQueue'
        settings["SCHEDULER_MEMORY_QUEUE"] = 'scrapy.squeues.FifoMemoryQueue'
    else:
        settings["DEPTH_PRIORITY"] = 0
        settings["SCHEDULER_DISK_QUEUE"] = 'scrapy.squeues.PickleLifoDiskQueue'
        settings["SCHEDULER_MEMORY_QUEUE"] = 'scrapy.squeues.LifoMemoryQueue'

    if download_params_form.get("ip_proxy") == 2:
        settings["MIDDLEWARES_PROXY_OPEN"] = True
    return settings