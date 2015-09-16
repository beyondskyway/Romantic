# -*- coding:utf8 -*-
__author__ = 'sky'

import os


SECRET_KEY = ''
CSRF_ENABLED = True
DEBUG = True


# 限定上传file小于2MB  by lee @ 14.7.21  17:54
MAX_CONTENT_LENGTH = 2 * 1024 * 1024

SEX = [(u'男', u'男'), (u'女', u'女')]

DEGREE = [(u'大专', u'大专'), (u'本科', u'本科'), (u'硕士', u'硕士'), (u'博士', u'博士')]

CONDITION = [(u'无房无车', u'无房无车'), (u'无房有车', u'无房有车'), (u'有房无车', u'有房无车'), (u'有房有车', u'有房有车')]

INCOME = [(u'3000元以下', u'3000元以下'), (u'3000-5000元', u'3000-5000元'), (u'5000-8000元', u'5000-8000元'), (u'8000元以上', u'8000元以上')]

STATUS = [(u'单身', u'单身'), (u'离异', u'离异'), (u'丧偶', u'丧偶'), (u'已婚', u'已婚')]


# MYSQL配置信息  by Lee 14.7.17 19:44
MYSQL_USER = 'root'
MYSQL_PASS = 'qwertyuiop'
MYSQL_HOST = '127.0.0.1'
MYSQL_HOST_S = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_DB = 'whwb'


# 迁移数据库。不是太懂，仅本地测试方便，线上不能用。 add by lee @ 14.7.23
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# 数据库备份 by skyway@14-9-2
BACKUP_TO_MAIL = ['']
BACKUP_STORAGE_NAME = ''
MAIL_SMTP = ('smtp.126.com', 25, '', '', False)

# SendCloud邮件配置
# SC_API_USER = ''
# SC_API_KEY = ''
SC_API_USER = ''
SC_API_KEY = ''
SEND_EMAIL = ''  # 发送平台邮件使用地址

# 方便其他地方使用 by skyway@14-9-4
if not 'SERVER_SOFTWARE' in os.environ:
    ENVIRONMENT = 'OFFLINE'
else:
    ENVIRONMENT = 'ONLINE'

# 环境检测 by Lee 14.7.17 19:44 modify by skyway@14-9-4
if ENVIRONMENT == 'OFFLINE':
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
    AVATARURL = "http://127.0.0.1:8080/upavatar"
else:
    from sae.const import (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
    AVATARURL = "http://whwb.vipsinaapp.com/upavatar"

# 源于SAE python Q&A 更改连接池，防止 MYSQL gone away
SQLALCHEMY_POOL_RECYCLE = 5


ORIGIN_BUCKET = ''
AVATAR_BUCKET = ''
# BACK_BUCKET = ''

QINIU_ACCESS_KEY = ''
QINIU_SECRET_KEY = ''
QINIU_DOMIN = ''