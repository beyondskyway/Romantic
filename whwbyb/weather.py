# -*- coding:utf8 -*-
# 5-17 skyway
import urllib2
import urllib
import json
import config


#获取星座运势
def get_astro(name):
    name_quote = urllib.quote(name.encode('utf8'))
    astro_url = 'http://apix.sinaapp.com/astrology/?appkey=trialuser&name=' + name_quote
    astro = urllib2.urlopen(astro_url).read()
    astro = astro[1:-1]
    re = astro.split('\\n')
    str = ""
    for i in re:
        if i == "":
            continue
        str += i + "\n"
    return str


#获得天气信息 5-17 by skyway
def get_weather(city, from_user, to_user):

    #city_quote = urllib.quote(city.decode(sys.stdin.encoding).encode('utf8'))
    city_quote = urllib.quote(city)
    #return city_quote
    weather_url = 'http://api.map.baidu.com/telematics/v3/weather?location='+ city_quote +'&output=json&ak=1107dd10033017a340a29cc5e52558e5'
    re = urllib2.urlopen(weather_url).read()
    re = re.decode('utf-8')
    weather = json.loads(re)['results']

    #当前
    city = weather[0]['currentCity']
    now_date = weather[0]['weather_data'][0]['date']
    now_dayPicUrl = weather[0]['weather_data'][0]['dayPictureUrl']
    now_nightPicUrl = weather[0]['weather_data'][0]['nightPictureUrl']
    now_weather = weather[0]['weather_data'][0]['weather']
    now_wind = weather[0]['weather_data'][0]['wind']
    now_temp = weather[0]['weather_data'][0]['temperature']
    #明天
    tomm_date = weather[0]['weather_data'][1]['date']
    tomm_dayPicUrl = weather[0]['weather_data'][1]['dayPictureUrl']
    tomm_nightPicUrl = weather[0]['weather_data'][1]['nightPictureUrl']
    tomm_weather = weather[0]['weather_data'][1]['weather']
    tomm_wind = weather[0]['weather_data'][1]['wind']
    tomm_temp = weather[0]['weather_data'][1]['temperature']
    #后天
    after_date = weather[0]['weather_data'][2]['date']
    after_dayPicUrl = weather[0]['weather_data'][2]['dayPictureUrl']
    after_nightPicUrl = weather[0]['weather_data'][2]['nightPictureUrl']
    after_weather = weather[0]['weather_data'][2]['weather']
    after_wind = weather[0]['weather_data'][2]['wind']
    after_temp = weather[0]['weather_data'][2]['temperature']
    #大后天
    last_date = weather[0]['weather_data'][3]['date']
    last_dayPicUrl = weather[0]['weather_data'][3]['dayPictureUrl']
    last_nightPicUrl = weather[0]['weather_data'][3]['nightPictureUrl']
    last_weather = weather[0]['weather_data'][3]['weather']
    last_wind = weather[0]['weather_data'][3]['wind']
    last_temp = weather[0]['weather_data'][3]['temperature']

    title = city + u'天气预报'
    now_title = now_date + now_weather + now_temp + now_wind
    tomm_title = tomm_date + tomm_weather + tomm_temp + tomm_wind
    after_title = after_date + after_weather + after_temp + after_wind
    last_title = last_date + last_weather + last_temp + last_wind
    
    city_name = 'wuhan'
    pm2_5 = get_pm2_5(city_name)
    
    header = config.MSG_IMG_TXT_HEADER % (from_user, to_user, '6')
    items = config.MSG_IMG_TXT_ITEM % (title, '', '', '') \
            + config.MSG_IMG_TXT_ITEM % (pm2_5, '', '', '') \
            + config.MSG_IMG_TXT_ITEM % (now_title, '',now_dayPicUrl,'') \
            + config.MSG_IMG_TXT_ITEM % (tomm_title, '',tomm_dayPicUrl,'') \
            + config.MSG_IMG_TXT_ITEM % (after_title, '',after_dayPicUrl,'') \
            + config.MSG_IMG_TXT_ITEM % (last_title, '',last_dayPicUrl,'')
    foot = config.MSG_IMG_TXT_FOOT % ('0')
    return header + items + foot


#获取PM2.5 5-18 by skyway
def get_pm2_5(city_name):
    pm2_5_content = u'空气质量指数：%s %s'
    pm_error = u'调皮的PM2.5不想让你知道当前状况'
    pm2_5_token = '9jEzJfNeq3f3x9fvZae2'
    pm2_5_url = 'http://www.pm25.in/api/querys/pm2_5.json?city='+ city_name + '&token=' + pm2_5_token + '&stations=no'
    re = urllib2.urlopen(pm2_5_url).read()
    re = re.decode('UTF-8')
    pm2_5 = json.loads(re)
    #是否出错
    try:
        if 'error'in pm2_5:
            #print pm2_5['error']
            return pm_error
        else:
            aqi = pm2_5[0]['aqi']
            area = pm2_5[0]['area']
            pm25 = pm2_5[0]['pm2_5']
            pm2_5_24h = pm2_5[0]['pm2_5_24h']
            quality = pm2_5[0]['quality']
            time_point = pm2_5[0]['time_point']
            content = pm2_5_content % (aqi, quality)
            return content
    except:
        return '啊噢，服务器出了点小问题，请稍后再试！'

# re =  get_astro(u"狮子座")
# print re