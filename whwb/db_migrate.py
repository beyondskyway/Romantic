# -*- coding: utf-8 -*-
__author__ = 'SkyWay'

import imp
from migrate.versioning import api
from myapp import db
from config import SQLALCHEMY_MIGRATE_REPO, SQLALCHEMY_DATABASE_URI


# 不记录版本迁移
def migration():
    api.update_db_from_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, db.metadata)
    return u'迁移成功！'


# 无法迁移，报错
def migrate():
    # 创建迁移文件
    migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI,
                                                                                         SQLALCHEMY_MIGRATE_REPO) + 1)
    # 新建模型
    tmp_module = imp.new_module('old_model')
    # 原来的模型
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    exec old_model in tmp_module.__dict__
    # 生成迁移脚本
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta,
                                              db.metadata)
    # 将更新脚本写入迁移文件
    open(migration, "wt").write(script)
    # 更新数据库到最新版本
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print u'New migration saved as ' + migration + \
           u'Current database version:' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

if __name__ == "__main__":
    # migrate()
    migration()