from nonebot import on_command,CommandSession
import re
import requests
import json

@on_command('weather',aliases=['天气','查天气','今日天气'])#后者是取别名
async def weather(session:CommandSession):
    city = session.get('city',prompt='你想查哪个城市呢？')
    #data = session.get('data',prompt='你想查那一天呢（格式：20190214）？')
    #获取当前的内容session.ctx

    #await session.send('你查询的日期是'+data)

@weather.args_parser#@交互式对话
async def _(session:CommandSession):
    if session.is_first_run:
        return
    cityname = session.current_arg_text
    citycode = None
    with open('_city.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
    for item in data:
        if item['city_name'] == cityname:
            citycode = item['city_code']
    if citycode:
        url1 = f'http://t.weather.sojson.com/api/weather/city/{citycode}'
    else:
        session.pause('城市名字错误!请重新输入')
    r = requests.get(url1)
    r.encoding = 'utf-8'
    r = r.json()
    data = r['data']
    city = r['cityInfo']['city']
    shidu = data['shidu']
    pm25 = data['pm25']
    pm10 = data['pm10']
    quality = data['quality']
    wendu = data['wendu']
    tishi = data['ganmao']
    a = data['forecast']  # 预告
    a = a[0]
    high = a['high']
    low = a['low']
    ymd = a['ymd']  # 日期
    week = a['week']
    sunrise = a['sunrise']
    sunset = a['sunset']
    aqi = a['aqi']  # 空气质量指数
    fx = a['fx']
    fl = a['fl']  # 凤级
    type = a['type']
    notice = a['notice']

    reply = f'城市:{city}\n日期:{ymd}\t{week}\n天气:{type}\n温度：{wendu}\n日出时间：{sunrise}\t日落时间{sunset}\n湿度:{shidu}\n最高气温{high}\t最低气温:{low}\n空气质量：{quality}\t空气质量指数{aqi}\n风向：{fx}\t凤级:{fl}\'' \
            f'\nPM2.5:{pm25}\n温馨提示：\n{tishi}\n{notice}'
    await session.send(reply)

    #if session.current_key == 'data' and session.current_key.isdigit():#判断是不是数字
        #if not re.match(r'^\d{8}$',session.current_arg_text):
        #if not re.fullmatch(r'^\d{8}',session.current_arg_text):
            #session.pause('日期格式不对，请重新输入')
            #session.pause('城市名字错误!)
    #session.args[session.current_key] = session.current_arg_text#将当前对话文本赋值给data


