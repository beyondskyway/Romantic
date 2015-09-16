# -*- coding:utf8 -*-
import urllib2
import json
import config


class Menu:
    accessUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+ config.APP_ID +"&secret=" + config.APP_SECRET
    delMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
    createUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="
    getMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token="
    accessToken = ""

    def getAccessToken(self):
        f = urllib2.urlopen(self.accessUrl)
        accessT = f.read().decode("utf-8")
        jsonT = json.loads(accessT)
        self.accessToken = jsonT["access_token"]
        return self.accessToken

    def delMenu(self):
        html = urllib2.urlopen(self.delMenuUrl + self.accessToken)
        result = json.loads(html.read().decode("utf-8"))
        return result["errcode"]

    def createMenu(self):
        re = urllib2.Request(self.createUrl + self.accessToken, config.MENU) #menu 移到setting by skyway 6-18
        html = urllib2.urlopen(re)
        result = json.loads(html.read().decode("utf-8"))
        return result["errcode"]

    def getMenu(self):
        html = urllib2.urlopen(self.getMenuUrl + self.accessToken)
        print(html.read().decode("utf-8"))

'''
#使用示例
wx = Menu()
print(wx.getAccessToken())
print(wx.delMenu())
#print(wx.createMenu())
wx.getMenu()
'''