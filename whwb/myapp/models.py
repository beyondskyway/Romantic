# -*- coding:utf8 -*-
# 2014.12.29
__author__ = 'skyway'

from myapp import db
import datetime

# 关注/粉丝表
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('timestamp', db.DateTime, default=datetime.datetime.now))


# 用户信息表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger)  # by skyway@14-11-22 随机6位数字+id,防止爬虫
    qq = db.Column(db.String(15), unique=True)
    # 是否加密
    password = db.Column(db.String(50))
    nickname = db.Column(db.String(20))
    sex = db.Column(db.String(5))
    age = db.Column(db.SmallInteger)
    height = db.Column(db.SmallInteger, default=0)
    degree = db.Column(db.String(10))
    condition = db.Column(db.String(10))
    department = db.Column(db.String(20))
    income = db.Column(db.String(10))
    introduce = db.Column(db.String(300))
    # 择偶要求
    requirement = db.Column(db.String(300))
    # 私人信息
    name = db.Column(db.String(30))
    phone = db.Column(db.String(50))
    identity_id = db.Column(db.String(30))
    # 喜欢数
    likes = db.Column(db.Integer, index=True, default=0)
    # 婚姻状态
    status = db.Column(db.String(2))

    # 权限 0：一般用户，1：上传头像用户，……，9：管理员，10：超级管理员
    role = db.Column(db.SmallInteger, default=0)
    avatar_path = db.Column(db.String(100), default="http://7u2k3x.com1.z0.glb.clouddn.com/404")
    # back_path = db.Column(db.String(100), default="http://background-thumb.qiniudn.com/404")
    last_seen = db.Column(db.DateTime, default=datetime.datetime.now)
    regtime = db.Column(db.Date, default=datetime.date.today)
    # 关注/粉丝
    followed = db.relationship('User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id==id),
        secondaryjoin = (followers.c.followed_id==id),
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic')

    # 私信
    messages = db.relationship('MsgContent', backref='author', lazy='dynamic')
    # 活动参与者
    paticipators = db.relationship('PaticipatorInfo', backref='actor', lazy='dynamic')

    # 下面四个method， 都是服务于 flask-login.
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    # 下面四个，关注/好友关系。 模仿microblog，考虑添加“好友” add by lee @ 14.7.25 11:05
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self      # 返回的一定是 User 的实例，这样才能 db.session.add(user)  comment by lee  #  狗屁！！

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id==user.id).count() > 0

    """这样会执行两次数据库查询。我觉得应该有更好的办法。譬如直接查询followers表？"""
    # add by lee @ 14.7.25 11:23
    def is_friend(self, user):
        return self.is_following(user) and user.is_following(self)

    def __repr__(self):
        return '<User %r>' % self.nickname


# 活动信息 by skyway@15-1-1
class ActivityInfo(db.Model):
    __tablename__ = 'activity_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    time = db.Column(db.String(50))
    address = db.Column(db.String(50))
    introduce = db.Column(db.String(500))
    guest = db.Column(db.String(50))
    # 活动海报
    poster = db.Column(db.String(300))
    # 添加时间
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)


# 报名信息 by skyway@15-1-1
class PaticipatorInfo(db.Model):
    __tablename__ = 'paticipator_info'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 报名时间
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)


# 私信对话 by skyway@14-8-13
class MsgSession(db.Model):
    __tablename__ = 'msg_session'
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_user = db.relationship(User,
                                primaryjoin='User.id==MsgSession.from_id',
                                backref=db.backref('from_session', cascade='all,delete-orphan'))
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user = db.relationship(User,
                              primaryjoin='User.id==MsgSession.to_id',
                              backref=db.backref('to_session', cascade='all,delete-orphan'))
    from_read = db.Column(db.Boolean, default=False)
    to_read = db.Column(db.Boolean, default=False)
    count = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, index=True)
    msg_contents = db.relationship('MsgContent', backref='session', lazy='dynamic')

    def latest_msg(self):
        body = self.msg_contents.filter(MsgContent.timestamp==self.timestamp).first() #不能使用filter_by
        return body.body

    def __repr__(self):
        return '<Session %r>' % (self.to_user)


# 私信消息 by skyway@14-8-13
class MsgContent(db.Model):
    __tablename__ = 'msg_content'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('msg_session.id'))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Content %r>' % (self.body)


# by skyway@14-8-31 存储备份信息
class BackUp(db.Model):
    __tablename__ = 'back_up'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer)
    file_name = db.Column(db.String(50))
    is_done = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True)