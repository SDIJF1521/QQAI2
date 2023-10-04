import json
import requests
with open('./qqai2/plugins/data/CityCode.json','r',encoding="UTF-8") as f:
    Data = json.load(f) #读取城市代码
class Weather:
    def __init__(self,city:str):
        CityData = Data.get(city)
        CityCode = ''
        # 确定对应城市代码
        if CityData == None:
            for i in Data:
                CityData = Data[i].get(city)
                if CityData != None:
                    CityCode = CityData.get(list(CityData.keys())[3])
                    break

        else:
            CityCode = CityData[list(CityData.keys())[0]].get(list(CityData[list(CityData.keys())[0]].keys())[0])
        if CityCode == '':
            for i in Data:
                for j in Data[i]:
                    for k in Data[i][j]:
                        if k == city:
                            CityCode = Data[i][j][k]
        self.CityCode = CityCode
    def Forecast(self):
        try:
            url = f'https://restapi.amap.com/v3/weather/weatherInfo?key=a2ef174159414b4f2d7a478d495097b2&city={self.CityCode}&extensions=all&all=json'
            urlDATA = requests.get(url).content    # 获取气象信息
            weatherdata = json.loads(urlDATA)['forecasts'][0]['casts']
            # 将气象信息整理并返回
            return f'- [CQ:face,id=189]日期：{weatherdata[0]["date"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 星期：{weatherdata[0]["week"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 天气：{weatherdata[0]["dayweather"]}转{weatherdata[0]["nightweather"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 白天风向：{weatherdata[0]["daywind"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 晚上风向：{weatherdata[0]["nightwind"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 风速：{weatherdata[0]["daypower"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 高温：{weatherdata[0]["daytemp_float"]}°c' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 低温：{weatherdata[0]["nighttemp_float"]}°c\n' \
                   f'- [CQ:face,id=189]日期：{weatherdata[1]["date"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 星期：{weatherdata[1]["week"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 天气：{weatherdata[1]["dayweather"]}转{weatherdata[0]["nightweather"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 白天风向：{weatherdata[1]["daywind"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 晚上风向：{weatherdata[1]["nightwind"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 风速：{weatherdata[1]["daypower"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 高温：{weatherdata[1]["daytemp_float"]}°c' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 低温：{weatherdata[1]["nighttemp_float"]}°c\n' \
                   f'- [CQ:face,id=189]日期：{weatherdata[2]["date"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 星期：{weatherdata[2]["week"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 天气：{weatherdata[2]["dayweather"]}转{weatherdata[0]["nightweather"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 白天风向：{weatherdata[2]["daywind"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 晚上风向：{weatherdata[2]["nightwind"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 风速：{weatherdata[2]["daypower"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 高温：{weatherdata[2]["daytemp_float"]}°c' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 低温：{weatherdata[2]["nighttemp_float"]}°c'
        except:
            return '小白查询不到结果＞︿＜'
    def now(self):
        try:
            url = f'https://restapi.amap.com/v3/weather/weatherInfo?key=a2ef174159414b4f2d7a478d495097b2&city={self.CityCode}&extensions=base&all=json'
            urlDATA = requests.get(url).content
            weatherdata = json.loads(urlDATA)['lives'][0]
            print(weatherdata)
            return f'- [CQ:face,id=189]日期：{weatherdata["reporttime"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 天气：{weatherdata["weather"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 当前风向：{weatherdata["winddirection"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 当前风速：{weatherdata["windpower"]}' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 当前温度：{weatherdata["temperature"]}°c' \
                   f'\u000a\u000a\t\t\t[CQ:face,id=190] 空气湿度：{weatherdata["humidity"]}'
        except:
            return '小白查询不到结果＞︿＜'
