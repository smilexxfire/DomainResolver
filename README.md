# DomainResolver
批量的域名、ip扫描系统，为分布式扫描子系统，提供域名、ip信息查询功能
## 使用
依赖于[资产管理子系统](https://github.com/smilexxfire/AssertManager)、[子域名扫描子系统](https://github.com/smilexxfire/SubdomainScan)

填入mongodb配置信息 `config/default.ini`

安装依赖 `pip install -r requirements.txt`

按需编辑`producer.py` 运行`python producer.py`启动扫描
## TODO
- [x] 域名dns查询，获取a、cname记录
- [x] 域名cdn判断
- [x] ip信息查询，cidr、asn、location、is_cdn