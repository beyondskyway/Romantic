# -*- coding:utf8 -*-
import time
from weather import get_weather
import config


def handle_event(xml_recv, from_user, to_user):
    event_type = xml_recv.find("Event").text
    #关注事件
    if event_type == 'subscribe':
        content = config.STR_SUB
    #取消关注
    elif event_type == 'unsubscribe':
        content = ''
    elif event_type == 'CLICK':
        event_key = xml_recv.find("EventKey").text
        #天气
        if event_key == 'WEATHER':
            city = '武汉'
            weather = get_weather(city, from_user, to_user)
            return weather
        #帮助
        elif event_key == 'HELP':
            content = config.STR_HELP
        #往期回顾
        elif event_key == 'REVIEW':
            header = config.MSG_IMG_TXT_HEADER % (from_user, to_user, '1')
            item = config.MSG_IMG_TXT_ITEM % (
                '往期回顾',
                '往期的各种丰富的线下同城活动……',
                'http://mmbiz.qpic.cn/mmbiz/68j2HjK6ejAmhTiahhZSyxzicOiaDicmbs8OQDRGgnhkWg8lbFOfVPSBHrQfTGDYQQM6GwENic7FLyaYf1qta0rMChg/0?tp=webp',
                'http://mp.weixin.qq.com/s?sn=e9058cab7bc308136b38e6aad910ce35&mid=202381233&idx=1&plg_auth=1&__biz=MzA3NDE4NzU3NQ%3D%3D#rd'
            )
            foot = config.MSG_IMG_TXT_FOOT % '0'
            return header + item + foot
        elif event_key == 'STAR':
            content = config.STR_STAR
        else:
            content = ''
    else:
        content = ''
    reply_msg = config.MSG_TXT % (from_user, to_user, str(int(time.time())), content)
    return reply_msg