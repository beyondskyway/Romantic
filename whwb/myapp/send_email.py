# -*- coding: utf-8 -*-
__author__ = 'SkyWay'

import config
from decorators import async
from flask import render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


if config.ENVIRONMENT == 'ONLINE':
    from sae.mail import send_mail
    from sae.mail import EmailMessage


# SendCloud发送邮件
def sc_mail(to_email, subject, html, from_email=config.SEND_EMAIL):
    # 基本信息
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    # 添加html到msg
    part = MIMEText(html, 'html', "utf-8")
    msg.attach(part)
    # 发送邮件
    smtp = smtplib.SMTP('smtpcloud.sohu.com:25')
    smtp.login(config.SC_API_USER, config.SC_API_KEY)
    smtp.sendmail(from_email, to_email, msg.as_string())
    smtp.quit()


# 快速邮件
def quick_mail(to, subject, body):
    send_mail(to, subject, body, config.MAIL_SMTP)


# Html形式邮件
@async
def html_mail(to, subject, html, smtp):
    em = EmailMessage()
    em.to = to
    em.subject = subject
    em.html = html
    em.smtp = smtp
    em.send()


# 关注邮件通知
def follow_notification(followed, follower):
    content = u"在武汉高校之恋中羞涩的关注了你！"
    html_mail(followed.email,
              u"关注提醒——武汉高校之恋",
              render_template("email.html", to_user=followed, from_user=follower, content=content), config.MAIL_SMTP)


# 私信邮件通知
def pri_msg_notification(from_user, to_user):
    content = u"在武汉高校之恋中给你发了一丢丢封私信！"
    html_mail(to_user.email,
              u"私信提醒——武汉高校之恋",
              render_template("email.html", to_user=to_user, from_user=from_user, content=content), config.GMAIL_SMTP)
