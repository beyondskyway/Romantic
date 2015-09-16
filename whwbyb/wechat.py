# -*- coding:utf8 -*-
# 2014.4.22 21:59 wnlo-c209
import string
import MySQLdb
from flask import Flask, g, request, make_response, render_template
import hashlib
import xml.etree.ElementTree as ET
from event import handle_event
from message import handle_msg
#6-1 skyway
from menu import*
import config
#from database import*

app = Flask(__name__)

#配置部分
#app.debug = True


from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)


@app.before_request
def before_request():
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB, port=int(MYSQL_PORT), charset='utf8')


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


#主程序
@app.route('/', methods=['GET', 'POST'] )
def wechat_auth():
    #微信验证
    if request.method == 'GET':
        token = config.APP_TOKEN  # app token
        query = request.args  # GET 方法附上的参数
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if hashlib.sha1(s).hexdigest() == signature:
            # print "success"
            return make_response(echostr)
    #获取XML消息内容
    xml_recv = ET.fromstring(request.data)
    msg_type = xml_recv.find('MsgType').text
    to_user = xml_recv.find("ToUserName").text
    from_user = xml_recv.find("FromUserName").text
    #菜单事件
    if msg_type == 'event':
        reply_msg = handle_event(xml_recv, from_user, to_user)
    #消息响应
    else:
        reply_msg = handle_msg(xml_recv, from_user, to_user)
    # print reply_msg
    response = make_response(reply_msg)
    response.content_type = 'application/xml'
    return response


#缘分社区
@app.route('/luckchance', methods=['POST', 'GET'])
def luckchance():
    return render_template('luckchance.html')


#活动报名
@app.route('/enroll', methods=['POST', 'GET'])
def enroll():
    return render_template('enroll.html')


#修改菜单
@app.route('/menu')
def menu():
    wx = Menu()
    print(wx.getAccessToken())
    print(wx.delMenu())
    print(wx.createMenu())
    wx.getMenu()
    return "菜单修改成功"