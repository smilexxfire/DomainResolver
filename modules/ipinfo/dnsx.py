# -*- coding: UTF-8 -*-
'''
@Project ：subdomainMonitor 
@File    ：dnsx.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/8/7 14:21 
@Comment ： 
'''
import json
import subprocess

from common.module import Module
from common.utils import rename_dict_key
from config.settings import data_storage_dir
from config.log import logger

class Dnsx(Module):
    def __init__(self, subdomains:list=None):
        self.module = "ipinfo"
        self.source = "dnsx"
        self.collection = "dns_record"
        self.index_field = "domain"
        self.cdn_cname_keywords_filename = data_storage_dir.joinpath("cdn_cname_keywords.json")

        Module.__init__(self,subdomains)

    def do_scan(self):
        """

        :return:
        """
        cmd = [self.execute_path, "-l", self.targets_file,  "-a", "-cname", "-j", "-o", self.result_file]
        subprocess.run(cmd)

    def deal_data(self):
        """
        处理扫描结果, 提取出所有记录并处理

        @return:
        """
        json_list = list()
        # 从文件中读取数据
        with open(self.result_file, "r") as f:
            datas = f.readlines()
            json_list = [json.loads(data) for data in datas]
            for data in json_list:
                # 删除一些key，避免keyerror，先set
                data.setdefault('resolver', None)
                del data["resolver"]
                data.setdefault('all', None)
                del data["all"]
                data.setdefault('soa', None)
                del data["soa"]

                rename_dict_key(data, "host", "domain")

        self.results = json_list

    def check_cdn(self):
        logger.log("INFOR", "Start check cdn")
        cdn_cname_keywords = json.loads(open(self.cdn_cname_keywords_filename, "r").read())
        for record in self.results:
            cnames = record.get("cname", None)
            if not cnames:
                return False
            # 遍历匹配
            for cname in cnames:
                if cname in cdn_cname_keywords.keys():
                    logger.log("INFOR", f"Matched domain {record['domain']} with cdn "
                                        f"{cname}: {cdn_cname_keywords[cname]}")
                    record["is_cdn"] = cdn_cname_keywords[cname]
                    break


    def save_db(self):
        super().save_db()

    def run(self):
        """
        入口执行函数

        :return:
        """
        self.begin()
        self.save_targets()
        self.do_scan()
        self.deal_data()
        self.check_cdn()
        self.save_db()
        self.finish()
        self.delete_temp()

def run(subdomains:list=None):
    dnsx = Dnsx(subdomains)
    dnsx.run()

if __name__ == '__main__':
    run(subdomains=["qiniu.xxf.world", "xxa.xxf.world", "me.xxf.world"])
