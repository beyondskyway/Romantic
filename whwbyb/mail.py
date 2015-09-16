# -*- coding:utf8 -*-
from sae.mail import send_mail
import config

# 向嘉宾请求，嘉宾的邮箱（已经移植到setting by skyway 6-18）
#GuestMail = {'1': '1440595207@qq.com', '2': '879331250@qq.com'}


#邮件服务，用于关注者给嘉宾发信息
def mail(address, body):
    subject = u'您好，有位来自武汉高校之恋的用户向你发送了交友请求'
    smtp = ('smtp.googlemail.com', '465', 'hugleecool@gmail.com', 'lihangcxf', True)
    send_mail(address, subject, body, smtp)


def guest_mail(content):
    if len(content) < 30:
        reply_msg = u'请求字数小于30字，被系统判定为无效内容'
        return reply_msg
    try:
        [nothing, guest, body] = content.split('@')
        address = config.GUEST_MAIL.get(guest)
        mail(address, body)
        reply_msg = u'您的交友请求已经发送至%s号嘉宾邮箱，期待你们的认识！~~\n\n温馨提示：长一点，正式一点的请求有助于嘉宾接受你哟~~' % guest
    except:
        reply_msg = u'您的交友请求失败了。可能原因：\n1.请求字数小于30字，被系统判定为无效内容\n2.你发送的嘉宾编号不存在，请查看嘉宾文章核对其编号\n3.编号前后有两个@，用于区分编号和请求内容\n4.系统错误，请加微信hugleecool反映情况'
    return reply_msg