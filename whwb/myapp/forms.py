# -*- coding:utf8 -*-
__author__ = 'skyway'

from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, PasswordField, SelectField, RadioField, DateField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired, Email, ValidationError, NumberRange
from config import DEGREE, SEX, CONDITION, INCOME, STATUS
from models import User, PaticipatorInfo


# 验证QQ的唯一性 by skyway@14-12-29
def qq_unique():
    message = u'该QQ号已经被使用'

    def _qq_unique(form, field):
        if User.query.filter_by(qq=field.data).first():
            raise ValidationError(message)
    return _qq_unique


# 登录表单
class LoginForm(Form):
    qq = StringField(u'QQ', validators=[Length(min=5, max=13, message=u'5到13位数字')])
    password = PasswordField(u'密码')


# 注册表单
class RegistryForm(Form):
    qq = StringField(u'QQ', validators=[Length(min=5, max=13, message=u'5到13位数字'), qq_unique()])
    password = PasswordField(u'密码', validators=[Length(min=5, max=20, message=u'5到20位密码')])
    nickname = StringField(u'昵称', validators=[Length(min=2, max=20, message=u'2到20位由汉字、数字、英文组成')])
    sex = RadioField(u'性别', choices=SEX, validators=[InputRequired(message=u'性别不能修改，如实填写~')])
    age = IntegerField(u'年龄', validators=[NumberRange(min=16, max=60, message=u'16到60数字')])
    degree = SelectField(u'学历', choices=DEGREE)
    condition = SelectField(u'房车', choices=CONDITION)
    department = StringField(u'单位', validators=[Length(min=2, max=20, message=u'2到20个字')])
    income = SelectField(u'月薪', choices=INCOME)
    introduce = TextAreaField(u'自我介绍', validators=[Length(max=300)])
    requirement = TextAreaField(u'择偶要求', validators=[Length(max=300)])
    status = SelectField(u'婚姻状态', choices=STATUS)

    name = StringField(u'姓名', validators=[Length(max=20)])
    phone = StringField(u'手机', validators=[Length(min=11, max=11, message=u"输入11位电话号码")])
    identity_id = StringField(u'身份证号', validators=[Length(min=18, max=18, message=u"输入18位身份证号")])


# 个人资料表单
class EditForm(Form):
    nickname = StringField(u'昵称', validators=[Length(min=2, max=20, message=u'2到20位由汉字、数字、英文组成')])
    age = IntegerField(u'年龄', validators=[NumberRange(min=16, max=60, message=u'16到60数字')])
    degree = SelectField(u'学历', choices=DEGREE)
    condition = SelectField(u'房车', choices=CONDITION)
    department = StringField(u'单位', validators=[Length(min=2, max=20, message=u'2到20个字')])
    income = SelectField(u'月薪', choices=INCOME)
    introduce = TextAreaField(u'自我介绍', validators=[Length(max=300)])
    requirement = TextAreaField(u'择偶要求', validators=[Length(max=300)])
    status = SelectField(u'婚姻状况', choices=STATUS)
    name = StringField(u'姓名', validators=[Length(max=20)])
    phone = StringField(u'手机', validators=[Length(min=11, max=11, message=u"输入11位电话号码")])


# 私信系统 by skyway@14-8-13
class MsgForm(Form):
    message = TextAreaField('message', validators=[Length(min=1, max=500, message=u"发送内容不能为空")])


# 找回密码 by skyway@14-9-23
class ForgetPwd(Form):
    qq = StringField('qq', validators=[Length(min=5, max=13, message=u'5到13位数字')])


# 活动信息 by skyway@14-8-17
class ActivityForm(Form):
    name = StringField(u'名称', validators=[Length(min=3, max=30, message=u'请输入3-20字')])
    time = StringField(u'时间', validators=[Length(min=2, max=40, message=u'请输入2-40字')])
    address = StringField(u'地点', validators=[Length(min=2, max=40, message=u'请输入2-40字')])
    introduce = TextAreaField(u'简介', validators=[Length(min=10, max=500, message=u'请输入10-500字')])
    guest = StringField(u'嘉宾', validators=[Length(min=2, max=40, message=u'请输入2-40字')])
    poster_url = StringField(u'海报链接', validators=[Length(min=0, max=300, message=u'请输入海报链接')])
