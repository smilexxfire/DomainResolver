# -*- coding: UTF-8 -*-
'''
@Project ：DomainResolver 
@File    ：ipcheck.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/9 15:26 
@Comment ： 
'''
import json
import ipaddress

from common.ipasn import IPAsnInfo
from common.ipreg import IpRegData
from common.module import Module
from config.settings import data_storage_dir
from config.log import logger

class IPInfo(Module):
    def __init__(self, ips):
        self.module = "ipinfo"
        self.source = "ipcheck"
        self.collection = "ip_info"
        self.index_field = "ip"
        # from https://github.com/al0ne/Vxscan/blob/master/lib/iscdn.py
        self.cdn_asn_list_filename = data_storage_dir.joinpath("cdn_asn_list.json")
        self.cdn_ip_cidr_filename = data_storage_dir.joinpath("cdn_ip_cidr.json")
        Module.__init__(self, ips)

    def do_scan(self):
        asn_info = IPAsnInfo()
        res = list()
        ipasninfo = IPAsnInfo()
        ipregdata = IpRegData()
        for ip in self.targets:
            ip_info = ipasninfo.find(ip=ip)
            ip_info.update(ipregdata.query(ip))
            ip_info["ip"] = ip
            self.results.append(ip_info)

    def check_cdn(self):
        cdn_asn_list = json.loads(open(self.cdn_asn_list_filename, "r").read())

        for record in self.results:
            ip = record["ip"]
            asn = record["asn"]
            if asn in cdn_asn_list or self.is_ip_cdn(ip):
                record["is_cdn"] = True
            else:
                record["is_cdn"] = False

    def is_ip_cdn(self, ip):
        cdn_ip_cidr_list = json.loads(open(self.cdn_ip_cidr_filename, "r").read())
        try:
            ip = ipaddress.ip_address(ip)
        except Exception as e:
            logger.log('DEBUG', e.args)
            return False

        for cidr in cdn_ip_cidr_list:
            if ip in ipaddress.ip_network(cidr):
                return True
        return False

    def save_db(self):
        super().save_db()

    def run(self):
        self.begin()
        self.do_scan()
        self.check_cdn()
        self.save_db()
        self.finish()
def run(ips:list):
    ipinfo = IPInfo(ips)
    ipinfo.run()

if __name__ == '__main__':
    run(["39.156.66.18"])
    # ip = IPInfo(ips=["14.0.59.2"])
    # print(ip.is_ip_cdn(ip="14.0.52.4"))
    # print(ip.is_ip_cdn(ip="47.245.105.155"))
