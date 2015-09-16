# -*- coding:utf8 -*-
__author__ = 'hugleecool'
# by skyway@14-8-14
from migrate.versioning import api
from config import SQLALCHEMY_MIGRATE_REPO
import os.path

# 14.7.23  进行flask-migrate修改，并未消化，再议

from config import SQLALCHEMY_DATABASE_URI

from myapp import db
# 修改 by lee @ 14.7.23 21:53
# 如果文件是以顶层文件执行，在启动时，__name__就会设置为字符串"__main__"
# 如果文件被导入，__name__就会改设成客户端所了解的模块名
# 麻痹的，我说为什么每次更新svn就要重新注册。我草，真危险，看来生产服务器的数据库一定要备份！！！


# by skyway@14-8-14 创建数据库和迁移版本
def create_db():
    db.session.rollback()
    db.drop_all()
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database_repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))


if __name__ == "__main__":
    create_db()
# import os.path
# if not 'SERVER_SOFTWARE' in os.environ:
#     from config import SQLALCHEMY_MIGRATE_REPO
#     if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
#         api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
#         api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
#     else:
#         api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))