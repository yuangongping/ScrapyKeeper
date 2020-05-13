import zipfile


def uzip(source_path, tar_path):
    zip_file = zipfile.ZipFile(source_path)
    zip_list = zip_file.namelist()  # 得到压缩包里所有文件
    for f in zip_list:
        zip_file.extract(f, tar_path)  # 循环解压文件到指定目录
    zip_file.close()  # 关闭文件，必须有，释放内存
