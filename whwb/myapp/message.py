# -*- coding: utf-8 -*-
__author__ = 'SkyWay'
import json
import requests


# "一小时活动"发送短信的脚本 add by lee @14.11.13
def send_message(phone, name, id, offline):
    phone = int(phone)
    # 有线下的机会
    if offline > 0.5:
        cid = "oO4wK038YYal"
    else:
        cid = "HLvSCt65YJT9"
    resp = requests.post(("http://api.weimi.cc/2/sms/send.html"),
    data={
        "uid": "pb055ijboNi5",
        "pas": "p7kqjf9t",
        "mob": phone,
        "cid": cid,
        "type": "json",
        "p1": name,
        "p2": id
    },timeout=12 , verify=False)
    result =  json.loads( resp.content )
    #print json.dumps(result).decode("unicode-escape")
    return result['code'],result['msg']
