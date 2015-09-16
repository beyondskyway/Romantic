# -*- coding:utf8 -*-
# 2015-1-1 by skyway
__author__ = 'SkyWay'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import jinja_filter

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'registry'
lm.login_message = u'赶紧注册吧，在这里你可以查看心仪的TA的资料，互发私信，认识更多朋友~'

app.jinja_env.filters['datetimeformat'] = jinja_filter.datetimeformat
app.jinja_env.filters['string_truncate'] = jinja_filter.string_truncate

# 否则找不到路由
import views, models