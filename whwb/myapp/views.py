# -*- coding:utf8 -*-
__author__ = 'hugleecool'

import random
from datetime import datetime, date, timedelta
from flask import render_template, g, redirect, url_for, request, flash, jsonify
from flask.ext.login import login_required, login_user, logout_user, current_user
from myapp import app, lm, db
from models import User, ActivityInfo
from forms import RegistryForm, LoginForm, EditForm, ActivityForm, MsgForm, ForgetPwd
import db_create
import db_migrate
import config
import time
from qiniu import conf, rs
import base64
import re   # add by lee @14.9.18
# by skyway@14-8-13
from models import MsgContent, MsgSession, BackUp, PaticipatorInfo
import json
import string
if config.ENVIRONMENT == 'ONLINE':
    from sae.deferredjob import MySQLImport, MySQLExport, DeferredJob, add
from send_email import quick_mail, html_mail, pri_msg_notification, follow_notification, sc_mail
from functools import wraps
from message import send_message


# 环境修饰器，通过@environment_required标记PC不允许访问的页面
def environment_required(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        if config.ENVIRONMENT == 'ONLINE':
            m = 'MicroMessenger'
            s = 'SAE'
            # 下面应该可以用一条更简洁优秀的正则表达式取代。求优化~   add by lee @14.9.19
            if not (re.findall(m, str(request.headers)) or re.findall(s, str(request.headers))):
                return render_template('qrcode.html')
        return f(*args, **kwargs)
    return decorated_fun


# 管理员修饰器
def admin_required(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        if config.ENVIRONMENT == 'ONLINE':
            if g.user.role not in [9, 10]:
                return render_template('403.html'), 403
        return f(*args, **kwargs)
    return decorated_fun


# 超级管理员修饰器
def super_admin_required(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        if config.ENVIRONMENT == 'ONLINE':
            if g.user.role < 10:
                return render_template('403.html'), 403
        return f(*args, **kwargs)
    return decorated_fun


""" 考虑使用toekn_loader作为用户的认证令牌，唯一识别用户，且不易通过用户的公开信息猜出 """
# user_loader回调，用于从会话中存储的用户ID重新加载用户对象。（看不懂，真心的。求教）
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    # # 检测是否为微信浏览器的请求。仅线上环境 add by lee @14.9.18 17:39
    # if config.ENVIRONMENT == 'ONLINE':
    #     m = 'MicroMessenger'
    #     s = 'SAE'
    #     # 下面应该可以用一条更简洁优秀的正则表达式取代。求优化~   add by lee @14.9.19
    #     if not (re.findall(m, str(request.headers)) or   re.findall(s, str(request.headers))):
    #         return render_template('qrcode.html')
    g.user = current_user
    # 每次访问都要操纵数据库，是不是对性能有影响？  by lee @ 14.7.20
    # if g.user.is_authenticated():
    #     # 禁用用户 by skyway@14-11-23
    #     if g.user.role == -1:
    #         flash(u'账号已注销或由于你的恶意访问或发送不良信息被举报而被禁用！')
    #         logout_user()
    #         return redirect(url_for('index'))


@app.teardown_request
def teardown_request(func):
    db.session.close()


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(qq=form.qq.data, password=form.password.data).first()
        # 是否存在
        if user is None:
            flash(u'你的用户名或密码错了，重新填写。如果实在忘记了，请联系管理员')
            return render_template('login.html', form=form)
        # 注销或禁用
        if user.role == -1:
            flash(u'账号已注销或由于你的恶意访问或发送不良信息被举报而被禁用！')
            return render_template('login.html', form=form)
        login_user(user, remember=True)
        return redirect(request.args.get("next") or url_for('index'))
    return render_template('login.html', form=form)


# 用户退出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# 用户注册 page 1：来自报名页面, 0 :其他
@app.route('/registry', methods=['GET', 'POST'])
@app.route('/registry/<int:page>', methods=['GET', 'POST'])
def registry(page=0):
    form = RegistryForm()
    if form.validate_on_submit():
        if request.form['height']:
            height = int(request.form['height'])
        else:
            height = 0
        g.user = User(qq=form.qq.data, password=form.password.data, nickname=form.nickname.data,
                      sex=form.sex.data, age=form.age.data, height=height, identity_id=form.identity_id.data,
                      degree=form.degree.data, condition=form.condition.data, department=form.department.data,
                      income=form.income.data, status=form.status.data, introduce=form.introduce.data,
                      requirement=form.requirement.data, name=form.name.data, phone=form.phone.data)
        db.session.add(g.user)
        db.session.commit()
        # by skyway@14-11-22 生成user_id
        pre = ''.join(random.sample(string.digits, 5))
        id_str = str(g.user.id) + pre
        g.user.user_id = int(id_str)
        db.session.add(g.user)
        # 自动关注自己   add by lee @ 14.7.26
        db.session.add(g.user.follow(g.user))
        # 自动关注官方账号  add by lee @ 14.9.10
        # db.session.add(g.user.follow(User.query.get(1)))
        # 自动在Visitors表里增加自己。 免得每次重复检测是否存在 add by lee @ 14.8.15"""
        # db.session.add(Visitors(user_id=g.user.id, visits=0))
        db.session.commit()
        login_user(g.user, remember=True)
        if page == 1:
            return redirect(url_for('enroll'))
        return redirect(url_for('upavatar'))
    return render_template('registry.html', form=form)


# 活动报名
@app.route('/enroll', methods=['GET', 'POST'])
@app.route('/enroll/<int:flag>', methods=['GET', 'POST'])
def enroll(flag=0):
    # 查询活动信息
    activity = ActivityInfo.query.order_by(ActivityInfo.id.desc()).first()
    # 点击立即报名响应
    if flag == 1:
        paticipator = PaticipatorInfo.query.filter_by(user_id=g.user.id, activity_id=activity.id).first()
        if paticipator is None:
            paticipator = PaticipatorInfo(activity_id=activity.id, user_id=g.user.id)
            db.session.add(paticipator)
            db.session.commit()
        return render_template('act_enroll.html', auth=1, activity=activity, share=1, number=paticipator.id)
        # 增加了查询次数
        # return redirect(url_for('enroll', flag=0))
    # 报名页面信息显示
    if flag == 0:
        # 用户已经登录，显示用户信息
        if g.user is not None and g.user.is_authenticated():
            paticipator = PaticipatorInfo.query.filter_by(user_id=g.user.id, activity_id=activity.id).first()
            if paticipator is None:
                return render_template('act_enroll.html', auth=1, activity=activity)
            else:
                return render_template('act_enroll.html', auth=1, activity=activity, share=1, number=paticipator.id)
        # 提示登录或注册
        else:
            return render_template('act_enroll.html', auth=0, activity=activity)


############ 将上传封装-以后可能用到： 头像、背景、相册 add by lee @14.8.22#############
# 修改@ 14.10.19 by lee
# 如果是本地压缩，七牛不处理图片的话：
# 只需写： update(bucket,'','',g.user.id,'',pipeline)
def update(orgin_bucket, target_bucket, returnUrl, user_id, oops, pipeline):
    conf.ACCESS_KEY = config.QINIU_ACCESS_KEY
    conf.SECRET_KEY = config.QINIU_SECRET_KEY

    key = str(datetime.now())[:19]+str(user_id)
    print key
    policy = rs.PutPolicy("%s:%s" % (orgin_bucket, key))
    policy.returnUrl = returnUrl
    policy.returnBody = '{"hash": $(etag), "key": "%s", "persistentId":"$(persistentId)"}'%key
    policy.mimeLimit = "image/*"
    policy.fsizeLimit = 12000000
    # 本地压缩后上传和原图直传，上传策略不一样  add by lee @14.9.21 21:28
    if oops != '':
        entry = target_bucket+':'+ key
        EncodeEntryURI = base64.urlsafe_b64encode(entry)
        # oops 举例：'imageView2/1/w/100/h/100/q/100|saveas/'
        Ops = oops + EncodeEntryURI
        policy.persistentOps = Ops
    policy.persistentPipeline = pipeline  # 为空表示使用公用队列，否则使用私用队列
    uptoken = policy.token()
    return uptoken, key


###############################
# 2014.10.19 add by lee   网页端传递图片压缩后的base64编码，后台转二进制然后上传七牛
@app.route('/upavatar', methods=['GET', 'POST'])
@login_required
def upavatar():
    uptoken, key = update(config.ORIGIN_BUCKET, config.AVATAR_BUCKET, config.AVATARURL, g.user.id, 'imageView2/1/w/100/h/100/q/100|saveas/', '')
    print uptoken
    if request.method=='POST':
        import base64
        import re
        data = request.form['data']
        # 正则提取。求更好的表达式 add by lee @14.9.21 18:45
        rdata = re.findall(r';base64,(.+)',data)[0]
        data =base64.b64decode(rdata)
        # 因为是服务器传七牛，遂取消回调，所以g.user.id其实意义不大
        import qiniu.io
        ret, err = qiniu.io.put(uptoken, key, data)
        print str(ret)
        if err is not None:
            print 'err:%s' % err
        g.user.avatar_path = "http://"+config.QINIU_DOMIN + key
        # 上传真实照片
        if g.user.role == 0:
            g.user.role = 1
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('profile', user_id=g.user.user_id))
    return render_template('upavatar.html')


# # 替换背景   by lee @ 14.8.22 22：12
# # 2014.10.19 add by lee   网页端传递图片压缩后的base64编码，后台转二进制然后上传七牛
# @app.route('/upback', methods=['GET', 'POST'])
# @login_required
# def upback():
#     uptoken, key = update(config.ORIGIN_BUCKET, config.BACK_BUCKET , config.BACKURL, g.user.id,
#                  'imageView2/1/w/400/h/250/q/100|saveas/', 'background' )
#     if request.method=='POST':
#         import base64
#         import re
#         data = request.form['data']
#         # 正则提取。求更好的表达式 add by lee @14.9.21 18:45
#         rdata = re.findall(r';base64,(.+)',data)[0]
#         data =base64.b64decode(rdata)
#         # 因为是服务器传七牛，遂取消回调，所以g.user.id其实意义不大
#
#         import qiniu.io
#         ret, err = qiniu.io.put(uptoken, key, data)
#         g.user.back_path = "http://"+config.BACK_BUCKET+".qiniudn.com/"+key
#         db.session.add(g.user)
#         db.session.commit()
#         return redirect(url_for('profile',user_id=g.user.user_id))
#     return render_template('upback.html')


# 编辑个人信息 page 1:来自报名，0：其他   by skyway@15-1-1
@app.route('/edit', methods=['GET', 'POST'])
@app.route('/edit/<int:page>', methods=['GET', 'POST'])
@login_required
def edit(page=0):
    form = EditForm()
    # 提交修改
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.age = form.age.data
        if request.form['height']:
            height = int(request.form['height'])
        else:
            height = 0
        g.user.height = height
        g.user.degree = form.degree.data
        g.user.condition = form.condition.data
        g.user.department = form.department.data
        g.user.income = form.income.data
        g.user.status = form.status.data
        g.user.introduce = form.introduce.data
        g.user.requirement = form.requirement.data
        g.user.name = form.name.data
        g.user.phone = form.phone.data
        db.session.add(g.user)
        db.session.commit()
        if page == 1:
            return redirect(url_for('enroll'))
        return redirect(url_for('profile', user_id=g.user.user_id))
    # 显示之前数据
    form.nickname.data = g.user.nickname
    form.age.data = g.user.age
    form.degree.data = g.user.degree
    form.condition.data = g.user.condition
    form.department.data = g.user.department
    form.income.data = g.user.income
    form.status.data = g.user.status
    form.introduce.data = g.user.introduce
    form.requirement.data = g.user.requirement
    form.name.data = g.user.name
    form.phone.data = g.user.phone
    return render_template('edit.html', form=form)


# 主页
@app.route('/')
@app.route('/index')
def index():
    # 24小时内登录的用户，按点赞数排行
    if g.user is not None and g.user.is_authenticated():
        # 根据登录用户性别选择
        if g.user.sex == u"男":
            users = User.query.filter(User.sex == u"女", User.last_seen > (datetime.now() - timedelta(days=3))).order_by(User.likes.desc()).limit(50).all()
        else:
            users = User.query.filter(User.sex == u"男", User.last_seen > (datetime.now() - timedelta(days=3))).order_by(User.likes.desc()).limit(50).all()
    else:
        users = User.query.filter(User.last_seen > (datetime.now() - timedelta(days=3))).order_by(User.likes.desc()).limit(50).all()
    # 生成json数据
    data = []
    for i in range(len(users)):
        tmp = {}
        tmp['nickname'] = users[i].nickname
        tmp['sex'] = users[i].sex
        tmp['age'] = users[i].age
        tmp['degree'] = users[i].degree
        tmp['img'] = users[i].avatar_path
        if users[i].sex == u"男":
            tmp['other'] = users[i].income
        else:
            tmp['other'] = users[i].height
        tmp['introduce'] = users[i].introduce
        tmp['introduce'] = tmp['introduce'][:15] + '...'
        tmp['last_seen'] = str(users[i].last_seen)
        tmp['url'] = url_for('profile', user_id=users[i].user_id)
        print tmp['url']
        tmp['last_seen'] = tmp['last_seen'][5:-3]
        print time
        data.append(tmp)
    json_str = json.dumps(data)
    length = len(json.loads(json_str))
    return render_template('index.html', users=json_str, length=length)


# 点击个人主页按钮 by skyway@15-1-3 用户未登录情况
@app.route('/userinfo')
def userinfo():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('profile', user_id=g.user.user_id))
    else:
        return redirect(url_for('registry'))


# 个人页面  add by lee @ 14.7.22 20:26
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        flash(u'该用户不在地球上')
        return render_template('index.html')
    # # 增加访客统计     add by lee @ 14.8.15
    # if g.user.id != user.id:
    #     u = Visitors.query.filter_by(user_id=user.id).first()
    #     u.visits = u.visits + 1
    #     db.session.add(u)
    #     db.session.commit()
    # counted=UserLikes.query.filter_by(likes_id=user.id).count()
    return render_template('profile.html', user=user)


# 点赞/喜欢
@app.route('/ajax/like/<int:user_id>')
@login_required
def like(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        db.session.add(g.user.follow(user))
        # 喜欢数加一
        user.likes += 1
        db.session.add(user)
        db.session.commit()
        return jsonify(count=user.likes)


# 取消喜欢
@app.route('/ajax/dislike/<int:user_id>')
@login_required
def dislike(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        db.session.add(g.user.unfollow(user))
        # 喜欢数减一
        user.likes -= 1
        db.session.add(user)
        db.session.commit()
        return jsonify(count=user.likes)


# 喜欢页面
@app.route('/likes')
@login_required
def likes():
    followers = g.user.followers.all()
    followed = g.user.followed.all()
    data = []
    for i in range(len(followers)):
        tmp = {}
        tmp['nickname'] = followers[i].nickname
        tmp['sex'] = followers[i].sex
        tmp['age'] = followers[i].age
        tmp['degree'] = followers[i].degree
        tmp['img'] = followers[i].avatar_path
        if followers[i].sex == u"男":
            tmp['other'] = followers[i].income
        else:
            tmp['other'] = followers[i].height
        tmp['introduce'] = followers[i].introduce
        tmp['introduce'] = tmp['introduce'][:15] + '...'
        tmp['last_seen'] = str(followers[i].last_seen)
        tmp['last_seen'] = tmp['last_seen'][5:-3]
        tmp['url'] = url_for('profile', user_id=followers[i].user_id)
        data.append(tmp)
    loveme = json.dumps(data)
    loveme_len = len(json.loads(loveme))
    data = []
    for i in range(len(followed)):
        tmp = {}
        tmp['nickname'] = followed[i].nickname
        tmp['sex'] = followed[i].sex
        tmp['age'] = followed[i].age
        tmp['degree'] = followed[i].degree
        tmp['img'] = followed[i].avatar_path
        if followed[i].sex == u"男":
            tmp['other'] = followed[i].income
        else:
            tmp['other'] = followed[i].height
        tmp['introduce'] = followed[i].introduce
        tmp['introduce'] = tmp['introduce'][:15] + '...'
        tmp['last_seen'] = str(followed[i].last_seen)
        tmp['last_seen'] = tmp['last_seen'][5:-3]
        tmp['url'] = url_for('profile', user_id=followed[i].user_id)
        data.append(tmp)
    ilove = json.dumps(data)
    ilove_len = len(json.loads(ilove))
    # 记录最近登录时间
    g.user.last_seen = datetime.now()
    db.session.add(g.user)
    db.session.commit()
    return render_template('likes.html', loveme=loveme, ilove=ilove, loveme_len=loveme_len, ilove_len=ilove_len)


# 匹配界面
@app.route('/match', methods=['GET', 'POST'])
@login_required
def match():
    # 提交筛选
    if request.form.get('match'):
        # 年龄
        begin_age = int(request.form.get('begin_age'))
        query = User.query.filter(User.age > (begin_age - 1))
        print begin_age
        print query.count()
        end_age = int(request.form.get('end_age'))
        query = query.filter(User.age < (end_age + 1))
        print end_age
        print query.count()
        # 身高
        height = request.form.get('height')
        query = query.filter(User.height > height)
        print height
        print query.count()
        # 收入
        income = request.form.get('income')
        if income == u"3000":
            query = query.filter((User.income == u'3000-5000元') | (User.income == u'5000-8000元')
                                 | (User.income == u'8000元以上'))
        elif income == u"5000":
            query = query.filter((User.income == u'5000-8000元') | (User.income == u'8000元以上'))
        elif income == u"8000":
            query = query.filter(User.income == u'8000元以上')
        print income
        print query.count()
        # 房车
        house = request.form.get('house')
        print house
        car = request.form.get('car')
        print car
        condition = u''
        if house == u'true':
            condition += u"有房"
        else:
            condition += u"无房"
        if car == u'true':
            condition += u"有车"
        else:
            condition += u"无车"
        print condition
        if condition == u"有房无车":
            query = query.filter((User.condition == u'有房无车') | (User.condition == u'有房有车'))
        elif condition == u"无房有车":
            query = query.filter((User.condition == u'无房有车') | (User.condition == u'有房有车'))
        elif condition == u"有房有车":
            query = query.filter(User.condition == u'有房有车')
        print query.count()
        # 学历
        degree = request.form.get('degree')
        if degree == u"本科":
            query = query.filter((User.degree == u'本科') | (User.degree == u'硕士') | (User.degree == u'博士'))
        elif degree == u"硕士":
            query = query.filter((User.degree == u'硕士') | (User.degree == u'博士'))
        elif degree == u"博士":
            query = query.filter(User.degree == u'博士')
        print degree
        print query.count()
        if g.user.sex == u"男":
            query = query.filter(User.sex == u"女")
        else:
            query = query.filter(User.sex == u"男")
        print query.count()
        users = query.order_by(User.last_seen.desc()).all()
        data = []
        for i in range(len(users)):
            tmp = {}
            tmp['nickname'] = users[i].nickname
            tmp['sex'] = users[i].sex
            tmp['age'] = users[i].age
            tmp['degree'] = users[i].degree
            tmp['img'] = users[i].avatar_path
            if users[i].sex == u"男":
                tmp['other'] = users[i].income
            else:
                tmp['other'] = users[i].height
            tmp['introduce'] = users[i].introduce
            tmp['introduce'] = tmp['introduce'][:15] + '...'
            tmp['last_seen'] = str(users[i].last_seen)
            tmp['last_seen'] = tmp['last_seen'][5:-3]
            tmp['url'] = url_for('profile', user_id=users[i].user_id)
            data.append(tmp)
        return json.dumps(data)
    if g.user.sex == u"男":
        begin_age = 20
        end_age = 35
        height = 155
        income = u"不限"
        degree = u"大专"
    else:
        begin_age = 20
        end_age = 40
        height = 168
        income = u"3000"
        degree = u"本科"
    return render_template('match.html', begin_age=begin_age, end_age=end_age, height=height, income=income, degree=degree)


# 关注某人  add by lee @14.7.22  edited by lee @14.7.25
@app.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    if g.user.user_id == user_id:
        flash(u'你不能关注你自己')
        return redirect(url_for('index'))
    else:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            db.session.add(g.user.follow(user))
            # n = Notify(type='follow', user_id=user.id)
            # 喜欢数加一
            user.likes += 1
            # db.session.add(n)
            db.session.add(user)
            # 删除关注私信by skyway@14-9-15
            # 关注邮件提醒by skyway@14-9-17 取消邮件发送by skyway@14-11-22
            # follow_notification(user, g.user)  # 减少邮件，已删除
            db.session.commit()
            return redirect(url_for('profile', user_id=user_id))
        else:
            flash(u'此用户不存在')
            return redirect(url_for('index'))


# 取消关注  add by lee @14.7.25
@app.route('/unfollow/<int:user_id>')
def unfollow(user_id):
    if g.user.user_id == user_id:
        flash(u'你不能取消关注你自己..不对..你是不是用爬虫登录的..诚实点我们还可以做朋友..微信hugleecool')
        return redirect(url_for('index'))
    else:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            db.session.add(g.user.unfollow(user))
            # 喜欢数减一
            user.likes -= 1
            db.session.add(user)
            db.session.commit()
            # flash(u'您已取消对TA的关注')
            return redirect(url_for('profile', user_id=user_id))
        else:
            flash(u'此用户不存在')
            return redirect(url_for('index'))


# #  生成用户
# @app.route('/create_user', methods=['GET', 'POST'])
# @login_required
# @super_admin_required
# def create_user():
#     for i in range(50000, 50500):
#         sex = random.choice([u'男', u'女'])
#         age = random.randint(16, 60)
#         height = random.randint(150, 250)
#         degree = random.choice([u'大专及以下', u'本科', u'硕士', u'博士'])
#         condition = random.choice([u'无房无车', u'无房有车', u'有房无车', u'有房有车'])
#         department = u"华科"
#         url = random.choice([u'http://avatar-thumb.qiniudn.com/2015-01-05 14:50:291',
#                              u'http://avatar-thumb.qiniudn.com/2015-01-05 09:52:092',
#                              u'http://avatar-thumb.qiniudn.com/2015-01-06 11:04:403',
#                              u'http://avatar-thumb.qiniudn.com/2015-01-06 00:11:06505',
#                              u'http://avatar-thumb.qiniudn.com/2015-01-07 15:33:20506',
#                              u'http://avatar-thumb.qiniudn.com/404'])
#         income = random.choice([u'3000元以下', u'3000-5000元', u'5000-8000元', u'8000元以上'])
#         introduce = u"啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦"
#         last_name = random.choice([u'胡', u'黄', u'王', u'李', u'金', u'陈', u'杨', u'高', u'张', u'马'])
#         first_name = random.choice([u'鸿煊', u'博涛', u'烨霖', u'烨华', u'航', u'壮', u'志强',
#                                     u'煜祺', u'智宸', u'正豪', u'昊然',
#                                     u'明杰', u'立诚', u'立轩', u'立辉',
#                                     u'峻熙', u'弘文', u'修洁', u'黎昕'])
#         nickname = last_name + first_name
#         name = u"哈哈"
#         phone = u'18986113139'
#         user = User(qq=i, password='123', nickname=nickname,
#                       sex=sex, age=age, height=height,
#                       degree=degree, condition=condition, department=department,
#                       income=income, introduce=introduce, name=name,
#                       phone=phone, avatar_path=url)
#         db.session.add(user)
#         db.session.commit()
#         # by skyway@14-11-22 生成user_id
#         pre = ''.join(random.sample(string.digits, 5))
#         id_str = str(user.id) + pre
#         user.user_id = int(id_str)
#         db.session.add(user)
#         # 自动关注自己   add by lee @ 14.7.26
#         db.session.add(user.follow(user))
#         db.session.add(Visitors(user_id=user.id, visits=0))
#         db.session.commit()
#     return u"用户创建成功！"


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


###################数据库操作###################

############  出于安全考虑，注释掉相关代码  add by lee @ 14.9.5########
'''有疑问。代码直接运行能工作，用网址打开，等很长时间，然后报错：
IntegrityError: (IntegrityError) (1062, "Duplicate entry '1@qq.com' for key 'email'")
初步猜想：
如果网页一直没响应，会重复发送请求，导致出错。求解答。
解决方案：尝试用多线程
UPDATE： Anthony建议不要在SAE上用多线程。
'''
############  出于安全考虑，注释掉相关代码  add by lee @ 14.9.5########

# by skyway @14-8-15
# # 创建数据库和版本
# @app.route('/admin/create')
# @super_admin_required
# def create():
#     db_create.create_db()
#     return "数据库创建成功"
#
#
# # 删除数据库
# @app.route('/admin/delete')
# @super_admin_required
# def delete():
#     db.drop_all()
#     return u'数据库已经删除！'


# 迁移数据库
@app.route('/admin/migrate')
@super_admin_required
def migrate():
    data = db_migrate.migration()
    return data


# 找回密码 by skyway@14-9-23
@app.route('/forget_pwd', methods=['GET', 'POST'])
def forget_pwd():
    form = ForgetPwd()
    if form.validate_on_submit():
        user = User.query.filter_by(qq=form.qq.data).first()
        if user is not None:
            email = user.qq + '@qq.com'
            content = u"您在武汉晚报遇见的账户信息如下："
            subject = u"找回密码——武汉晚报遇见"
            html = render_template("login_info_email.html", user=user, content=content)
            sc_mail([email], subject, html)
            flash(u"用户名和密码已发送到QQ邮箱！可能会被误认为垃圾邮件，确定没收到请加微信BeyondSkyWay")
            return redirect(url_for('login'))
        else:
            flash(u"该用户不存在！")
    return render_template("forget_pwd.html", form=form)


# 备份数据库到Storage
# 只能一个表一个表的导出，导出任务不会立刻执行（24h内）
@app.route('/admin/backup')
def backup():
    backup_time = datetime.now()
    time_str = backup_time.strftime('%Y-%m-%d-%H:%M:%S')  # 文件名不能有空格，否则mysql导出报错
    deferred_job = DeferredJob()
    notice = u'备份时间：%s<br>' % time_str
    # 添加备份任务并记录到数据库
    filename = "{}.sql.zip".format(time_str)
    #table_name为空时表示备份整个数据库
    job = MySQLExport(config.BACKUP_STORAGE_NAME, filename, '', '')
    job_id = deferred_job.add(job)
    notice += u'ID：%s, 文件名：%s<br>' % (job_id, filename)
    backup = BackUp(job_id=job_id, timestamp=backup_time, file_name=filename)
    db.session.add(backup)
    db.session.commit()
    notice = u'备份提交！<br>%s' % notice
    # 发送备份提交邮件
    html_mail(config.BACKUP_TO_MAIL, 'whwb-数据库备份', notice, config.MAIL_SMTP)
    return notice


# by skyway@14-8-31 数据库备份状态查询并发送邮件
@app.route('/admin/backup_status')
def backup_status():
    deferred_job = DeferredJob()
    latest_backup = BackUp.query.order_by(BackUp.timestamp.desc()).first()
    notice = u"备份时间：%s<br>" % str(latest_backup.timestamp)
    # 查询数据库保存的备份状态
    if latest_backup.is_done:
        # html_mail(config.BACKUP_TO_MAIL, 'whlove-数据库备份', u'备份已完成，邮件已发送！')
        return u'备份已完成，邮件已发送！'
    # 向服务器查询备份状态
    status = deferred_job.status(latest_backup.job_id)
    notice += u"文件名：%s, ID：%s, 状态：%s<br>" % (latest_backup.file_name, str(latest_backup.job_id), status)
    # 修改备份状态, 完成备份发送邮件
    if status == 'done':
        latest_backup.is_done = True
        db.session.add(latest_backup)
        db.session.commit()
        notice = u'备份已完成！<br>%s' % notice
        html_mail(config.BACKUP_TO_MAIL, 'whwb-数据库备份', notice, config.MAIL_SMTP)
        return notice
    else:
        return u'备份未完成！<br>%s' % notice


###################私信系统###################
# by skyway@15-1-3

#消息对话
@app.route('/session/', methods=['GET', 'POST'])
@login_required
def session():
    # 查询所有的消息对话
    sessions = MsgSession.query.\
        filter((MsgSession.from_id == g.user.id) | (MsgSession.to_id == g.user.id)).\
        order_by(MsgSession.timestamp.desc()).all()
    # 消息提醒系统    add by lee @ 14.8.15
    # Notify.query.filter_by(type='message', user_id=g.user.id).delete()
    # db.session.commit()
    return render_template("msg_session.html",
                           title=u'私信',
                           sessions=sessions)


#消息列表及发送
@app.route('/message/<int:user_id>', methods=['GET', 'POST'])
@login_required
def message(user_id):
    # 避免给自己发私信
    if g.user.user_id == user_id:
        flash(u'不能给自己发私信！')
        return redirect(url_for('profile', user_id=g.user.user_id))
    form = MsgForm()
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        flash(u'用户不存在！')
        return redirect(url_for('index'))
    # 查询msg_session
    if g.user.id > user.id:
        session = MsgSession.query.filter_by(from_id=g.user.id, to_id=user.id).first()
    else:
        session = MsgSession.query.filter_by(from_id=user.id, to_id=g.user.id).first()
    # 提交数据
    if form.validate_on_submit():
        # 创建msg_session
        if session is None:
            if g.user.id > user.id:
                session = MsgSession(from_id = g.user.id,
                                     to_id = user.id)
            else:
                session = MsgSession(from_id = user.id,
                                     to_id = g.user.id)
        else:
            session.count += 1
        timestamp = datetime.now()                        #  edit by lee  不要用utcnow。  @14.8.20
        msg = MsgContent(body = form.message.data, timestamp = timestamp, session = session, author = g.user)
        session.timestamp = timestamp
        # 标记未读状态
        if g.user.id == session.from_id:
            session.from_read = True
            session.to_read = False
        else:
            session.to_read = True
            session.from_read = False
        db.session.add(session)
        db.session.add(msg)
        # """增加私信提醒:Notify   add by lee @ 14.8.15"""
        # db.session.add(Notify(type='message', user_id=user.id))
        # 发送私信提醒邮件 by skyway@14-9-17
        # pri_msg_notification(g.user, user)
        db.session.commit()
        # flash(u'消息已发送！')  不需要，因为页面刷新后会自动显示出来
        return redirect(url_for('message', user_id=user_id))
    # by skyway@14-9-15 避免有session无content时报错
    # 存在对话
    if session:
        messages = session.msg_contents.order_by(MsgContent.timestamp).all()
        # 取消未读状态
        if g.user.id == session.from_id:
            session.from_read = True
        else:
            session.to_read = True
        db.session.add(session)
        db.session.commit()
    # 不存在对话messages为空
    else:
        messages = ''
    return render_template("msg_content.html",
                           title=u'私信',
                           form=form,
                           messages=messages,
                           user=user)


###########################后台管理###########################
@app.route('/admin', methods=['POST', 'GET'])
@login_required
@admin_required
def admin():
    return redirect(url_for('add_activity'))


#添加活动 by skyway@15-1-1
@app.route('/admin/add_activity', methods=['GET', 'POST'])
@login_required
@admin_required
def add_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = ActivityInfo(name=form.name.data,
                                time=form.time.data,
                                address=form.address.data,
                                introduce=form.introduce.data,
                                guest=form.guest.data,
                                poster=form.poster_url.data)
        db.session.add(activity)
        db.session.commit()
        flash(u'活动添加成功！')
        return redirect(url_for('add_activity'))
    return render_template("admin/add_activity.html",
                           title=u'活动',
                           form=form)


#活动修改 by skyway@15-1-1
@app.route('/admin/edit_activity', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_activity():
    activities = ActivityInfo.query.order_by(ActivityInfo.timestamp.desc()).all()
    # 查询活动
    if request.form.get('query_name'):
        name = request.form.get('query_name')
        activity = ActivityInfo.query.filter_by(name=name).order_by(ActivityInfo.timestamp.desc()).first()
        form = ActivityForm()
        form.name.data = activity.name
        form.time.data = activity.time
        form.address.data = activity.address
        form.introduce.data = activity.introduce
        form.guest.data = activity.guest
        form.poster_url.data = activity.poster
        return render_template('admin/edit_activity.html', activities=activities, form=form, id=activity.id)
    # 确认修改
    if request.form.get('edit'):
        activity_id = request.form.get('edit')
        activity = ActivityInfo.query.filter_by(id=activity_id).first()
        activity.name = request.form.get('name')
        activity.time = request.form.get('time')
        activity.address = request.form.get('address')
        activity.introduce = request.form.get('introduce')
        activity.guest = request.form.get('guest')
        activity.poster = request.form.get('poster_url')
        db.session.add(activity)
        db.session.commit()
        flash(u'活动修改成功！')
        form = ActivityForm()
        form.name.data = activity.name
        form.time.data = activity.time
        form.address.data = activity.address
        form.introduce.data = activity.introduce
        form.guest.data = activity.guest
        return render_template('admin/edit_activity.html', activities=activities, form=form, id=activity.id)
    return render_template('admin/edit_activity.html', activities=activities)


#活动管理 by skyway@15-1-2
@app.route('/admin/activity_info', methods=['GET', 'POST'])
@login_required
@admin_required
def activity_info():
    activities = ActivityInfo.query.order_by(ActivityInfo.timestamp.desc()).all()
    if request.form.get('name'):
        name = request.form.get('name')
        activity = ActivityInfo.query.filter_by(name=name).first()
        paticipators = PaticipatorInfo.query.filter_by(activity_id=activity.id).all()
        return render_template('admin/activity_info.html', activities=activities, activity=activity, paticipators=paticipators)
    return render_template('admin/activity_info.html', activities=activities)


#用户管理 by skyway@15-1-12
@app.route('/admin/user_info', methods=['GET', 'POST'])
@login_required
@admin_required
def user_info():
    if request.form.get('query'):
        info = request.form.get('query')
        users = User.query.filter((User.qq == info) | (User.phone == info))
        # if users is None:  # 不会进入
        if users.count() == 0:
            flash(u"啊哦，用户不存在！确定输入的号码是对的？")
            return render_template('admin/user_info.html')
        return render_template('admin/user_info.html', users=users)
    return render_template('admin/user_info.html')