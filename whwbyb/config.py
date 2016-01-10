# -*- coding:utf8 -*-
# by skyway@14-12-28

#################常量定义#################

#微信
# APP_ID = ''
# APP_SECRET = ''

APP_ID = ''
APP_SECRET = ''
APP_TOKEN = ''

#欢迎语
STR_SUB = """
欢迎关注“xxx”！我们是武汉乃至全国最具影响力的婚恋服务平台，期待您的持续关注。
点击您可直接回复来与我们交流，也可通过历史消息查看之前的文章……
"""

#帮助
STR_HELP = """
回复'h'或'帮助'呼出帮助菜单：

┄点击<a href="">我要相亲</a>，可直接报名参加线下活动
┄点击<a href="">缘分社区</a>，可进入我们的缘分社区畅聊

┄回复'tq'可查看最近天气情况

┄回复其他内容，我们后台也能看到。当回复内容的开头为'重要'时，你的消息会成为星标消息
┄想咨询更多？请加QQ:2118892572。
"""

#星座消息
STR_STAR = """
输入以下星座名称，即可获得今天星座运势：
白羊座
金牛座
双子座
巨蟹座
狮子座
处女座
天秤座
天蝎座
射手座
摩羯座
水瓶座
双鱼座
"""

STAR_INFO = (u'白羊座', u'金牛座', u'双子座', u'巨蟹座', u'狮子座', u'处女座',
             u'天秤座', u'天蝎座', u'射手座', u'摩羯座', u'水瓶座', u'双鱼座')


#################消息结构#################

#文本消息
MSG_TXT = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>'''

#图文消息
MSG_IMG_TXT_HEADER = """
<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>%s</ArticleCount>
    <Articles>
"""

MSG_IMG_TXT_ITEM = """
<item>
    <Title><![CDATA[%s]]></Title>
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
</item>
"""

MSG_IMG_TXT_FOOT = """</Articles>
<FuncFlag>%s</FuncFlag>
</xml> """

#################菜单结构#################
MENU = """
{
    "button":[
    {
        "name":"同城活动",
        "sub_button":[
        {
            "type":"view",
            "name":"我要相亲",
            "url":""
        },
        {
            "type":"view",
            "name":"往期回顾",
            "url":""
        }]
    },
    {
        "type":"view",
        "name":"缘分社区",
        "url":""
    },
    {
        "name":"更多惊喜",
        "sub_button":[
        {
            "type":"view",
            "name":"求助",
            "url":""
        },
        {
            "type":"click",
            "name":"星座运势",
            "key":"STAR"
        },
        {
            "type":"view",
            "name":"甜蜜兑换券",
            "url":""
        },
        {
            "type":"view",
            "name":"关于我们",
            "url":""
        }]
    }]
}
"""
