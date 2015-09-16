# -*- coding:utf8 -*-
import time
from weather import get_weather, get_astro
import config


def handle_msg(xml_recv, from_user, to_user):
    content = xml_recv.find('Content').text
    # 天气
    if content == 'tq':
        city = '武汉'
        weather = get_weather(city, from_user, to_user)
        print weather
        return weather
    # 帮助
    elif content == u'h' or content == u"帮助":
        reply_msg = config.STR_HELP
    # 星座
    elif content in config.STAR_INFO:
        reply_msg = get_astro(content)
    else:
        reply_msg = u'谢谢你的回复与关注！小姻会在后台看到你的消息，欢迎注册缘分社区，在那寻求你的另一半，有疑问可以加QQ：2118892572咨询[调皮]~~'
    reply_msg = config.MSG_TXT % (from_user, to_user, str(int(time.time())), reply_msg)
    return reply_msg