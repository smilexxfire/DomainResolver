# -*- coding: UTF-8 -*-
'''
@Project ：DomainResolver 
@File    ：producer.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/11 1:53 
@Comment ： 启动扫描任务
'''

from modules.domainresolve import DomainResolver

if __name__ == '__main__':
    domainResolver = DomainResolver()
    # domainResolver.dns_resolver_from_domain("baidu.com")
    # domainResolver.dns_resolver_from_assert("百度")
    # domainResolver.ipinfo_resolver_from_domain("baidu.com")
    # domainResolver.ipinfo_resolver_from_assert("百度")