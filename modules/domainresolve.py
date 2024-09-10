# -*- coding: UTF-8 -*-
'''
@Project ：subdomainMonitor 
@File    ：domainresolve.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/8/11 11:16 
@Comment ： 
'''
from config.log import logger
from common.database.db import conn_db
from modules.ipinfo import dnsx, ipcheck

class DomainResolver(object):
    def __init__(self):
        pass
    def get_subdomains_from_domain(self, domain):
        db = conn_db("subdomain")
        subdomains = db.find({"domain": domain})
        subdomain_values = [doc.get("subdomain") for doc in subdomains]
        return subdomain_values

    def get_subdomains_from_assert(self, assert_name):
        db = conn_db("asserts")
        # 第一步：在 asserts 集合中根据 assert_name 查找所有文档
        assert_docs = db.find({"assert_name": assert_name})
        # 提取所有的 domain 字段
        domains = [doc.get("domain") for doc in assert_docs if doc.get("domain")]
        if not domains:
            return f"No documents found with assert_name: {assert_name} or no domain fields."
        db = conn_db("subdomain")
        # 第二步：在 subdomain 集合中查找所有与 domain 匹配的 subdomain
        subdomains = db.find({"domain": {"$in": domains}})
        # 提取 subdomain 值
        subdomain_values = [doc.get("subdomain") for doc in subdomains]
        return subdomain_values

    def get_ips_from_domain(self, domain):
        subdomains = self.get_subdomains_from_domain(domain)
        db = conn_db("dns_record")
        ips = db.find({"domain": {"$in": subdomains}})
        ips_values = [value for doc in ips for value in doc.get("a", [])]
        return list(set(ips_values))

    def get_ips_from_assert(self, assert_name):
        subdomains = self.get_subdomains_from_assert(assert_name)
        db = conn_db("dns_record")
        ips = db.find({"domain": {"$in": subdomains}})
        ips_values = [value for doc in ips for value in doc.get("a", [])]
        return list(set(ips_values))

    def dns_resolver_from_domain(self, domain):
        '''
        获取domain的所有子域，并进行dns解析

        :param domain: 主域名
        :return:
        '''
        logger.log("INFOR", "Start dns_resolver_from_domain module")
        subdomains = self.get_subdomains_from_domain(domain)
        logger.log("INFOR", f"Get {len(subdomains)} subdomains from domain: {domain}")
        dnsx.run(subdomains=subdomains)

    def dns_resolver_from_assert(self, assert_name):
        '''
        获取资产下的所有子域名，并进行dns解析

        :param assert_name: 资产名
        :return:
        '''
        logger.log("INFOR", "Start dns_resolver_from_assert module")
        subdomains = self.get_subdomains_from_assert(assert_name)
        logger.log("INFOR", f"Get {len(subdomains)} subdomains from assert: {assert_name}")
        dnsx.run(subdomains=subdomains)

    def ipinfo_resolver_from_domain(self, domain):
        '''
        获取domain下的所有ip（子域名解析出来的）,进行ip信息查询

        :param domain: 主域名
        :return:
        '''
        logger.log("INFOR", "Start ipinfo_resolver_from_domain module")
        ips = self.get_ips_from_domain(domain)
        logger.log("INFOR", f"Get {len(ips)} ip from domain: {domain}")
        ipcheck.run(ips=ips)

    def ipinfo_resolver_from_assert(self, assert_name):
        '''
        获取资产下的所有ip（子域名解析出来的）,进行ip信息查询

        :param assert_name:
        :return:
        '''
        logger.log("INFOR", "Start ipinfo_resolver_from_assert module")
        ips = self.get_ips_from_assert(assert_name)
        print(ips)
        logger.log("INFOR", f"Get {len(ips)} ip from assert: {assert_name}")
        ipcheck.run(ips=ips)


if __name__ == '__main__':
    # DomainResolver().get_subdomains_from_domain(domain="lenovo.com")
    # print(DomainResolver().get_subdomains_from_assert(assert_name="百度"))
    # print(DomainResolver().get_ips_from_domain("baidu.com"))
    # DomainResolver().dns_resolver_from_domain("baidu.com")
    # DomainResolver().dns_resolver_from_assert("字节跳动")
    # DomainResolver().ipinfo_resolver_from_domain("baidu.com")
    # DomainResolver().ipinfo_resolver_from_assert("字节跳动")
    pass
