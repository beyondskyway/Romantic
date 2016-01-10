WHWB
---
基于Python+Flask，部署在SAE上的大型恋爱、交友社区

Deployment
---
- 使用SAE的Storage+Cron+DeferredJob+MySQL和SQLAlchemy开发环境
- 基于SendCloud邮件服务的的邮件系统
- 采用Bootstrap+Jinja2的前端框架模式
- 采用七牛图片云存储服务

##Config
---
- 配置`config.py`中与Flask、数据库、邮件、迁移、七牛等信息
- 通过`/create`创建数据库和迁移版本


##Docs


###Atention
- 数据库迁移牵涉外键、索引、默认值需逐步迁移


###Modify Log


##WEBsite
演示网站：

