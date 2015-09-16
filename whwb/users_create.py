# -*- coding:utf8 -*-
# 14.7.26 20:59
__author__ = 'hugleecool'


from myapp import db
from myapp.models import User, Visitors
import random
import time


# 学校列表：
schools = [school for (school, x) in ""]
sex = [u'男', u'女']
status = [u'本科生', u'研究生', u'已工作']


def users_create():
    t1 = time.clock()
    for i in range(1, 1000):
        ui = unicode(i)
        u = User(email=ui+u'@qq.com', password=u'123', nickname=ui+u'q',
                    school=random.choice(schools), sex=random.choice(sex), status=random.choice(status), grade=u'国光13级硕士',
                    bday=u'1992-03-14', pubinfo=u'我的邮箱是123457568', contact=u'微信：6578678687', prinfo=u'我有很多很多秘密')
        db.session.add(u)
        db.session.add(u.follow(u))
        db.session.commit()   # 必须先提交。不然下面找不到id
        """自动在Visitors表里增加自己。 免得每次重复检测是否存在 add by lee @ 14.8.15"""
        db.session.add(Visitors(user_id=u.id, visits=0))
    db.session.commit()
    t2 = time.clock()
    return t2 -t1

    #print u'创建用户耗时：%s秒，提交数据库耗时%s秒' % (delta1,delta2)

if __name__ == '__main__':
    print u'开始创建随机用户'
    users_create()
