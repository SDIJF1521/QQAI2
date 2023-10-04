import re
import json
import sqlite3
import os
import pymysql
import requests
def file(PORT,HOST = '127.0.0.1', name='XB', admin='12345678'):                                 #yml配置执行函数
    with open('./QQAI2/.env.prod', 'r', encoding='utf-8') as env1:
        data = env1.read()
        print(data)
        data_host = re.sub(re.findall(re.compile('HOST=(\d+.\d+.\d+.\d+)'), data)[0], str(HOST), data)
        data_port = re.sub(re.findall(re.compile('PORT=(\d+)'), data)[0], str(PORT), data_host)
        data_name = re.sub(re.findall(re.compile('NICKNAME=\["(\w+)"'), data_port)[0], name, data_port)
        data = re.sub(re.findall(re.compile('SUPERUSERS=\["(\d+)"'), data_name)[0], admin, data_name)
        print(data)
    with open('./QQAI2/.env.prod', 'w', encoding='utf-8') as env2:
        env2.write(data)
    with open('./QQAI2/.env.dev', 'r', encoding='utf-8') as env:
        data_env = env.read()
        print(data)
        data_host = re.sub(re.findall(re.compile('HOST=(\d+\.\d+\.\d+\.\d+)'), data_env)[0], str(HOST), data_env)
        data_port = re.sub(re.findall(re.compile('PORT=(\d+)'), data_host)[0], str(PORT), data_host)
        print(data_port)
    with open('./QQAI2/.env.dev', 'w', encoding='utf-8') as env:
        env.write(data_port)
def data(data='json'):            #json配置执行函数
    print(data)
    data_file = './QQAI2/qqai2/plugins/data'
    if not os.path.exists('./QQAI2/qqai2/plugins/data'):
        os.mkdir(data_file)
    if data == 'sqlite':                                        #sqlite数据库配置
        if not os.path.exists('./QQAI2/qqai2/plugins/data/data.db'):
            conn = sqlite3.connect('./QQAI2/qqai2/plugins/data/data.db')
            cursor = conn.cursor()
            with open('./config.json', 'r',encoding='UTF-8') as config_js:
                config_json = json.load(config_js)
                print(config_json)
            for i in config_json['sqlite']:
                cursor.execute(config_json['sqlite'][i])
    elif data == 'mysql':                                       #mysql数据库配置
        with open('./config.json', 'r',encoding='UTF-8') as config_js:
            config_json = json.load(config_js)
            print(config_json['mysql']['host'])
        conn = pymysql.connect(
            host=config_json['mysql']['host'],
            user=config_json['mysql']['user'],
            password=config_json['mysql']['password'])
        cursor = conn.cursor()
        cursor.execute(config_json['mysql']['创建数据库'])           #创建数据库
        cursor.close()
        conn.close()
        conn = pymysql.connect(
            host=config_json['mysql']['host'],
            user=config_json['mysql']['user'],
            password=config_json['mysql']['password'],
            database=config_json['mysql']['数据库']
        )
        cursor = conn.cursor()
        print('数据库连接成功')
        for i in config_json['mysql']['建表']:                         #创建表
            cursor.execute(config_json['mysql']['建表'][i])
            print('ok')
        cursor.close()
        conn.close()
    elif data == 'json':                                             #json数据配置
        print('ok')
        with open('./QQAI2/qqai2/plugins/data/data.json', 'w', encoding="UTF-8") as f:
            DATA = {'qd': {
                            'user': [],
                            '积分': [],
                            '日期': [],
                            '天数': []
                        },
                    'cq': {
                        'user': [],
                        'id':[],
                    '日期': []
                    },
                    'web': {
                        'name': [],
                        'url': []
                    },
                'sgin': {
                    'id': [],
                    '签诗': [],
                    '解签': []
                },
                'packsack':{},
                'favorability':{}}
            json.dump(DATA, f, indent=4,ensure_ascii=False)
    with open('./QQAI2/qqai2/plugins/data/reply.json', 'w', encoding="UTF-8") as reply:
        reply_DATA = {'name': [],
                      'function': [],
                      'time': []}
        json.dump(reply_DATA, reply, indent=4)
    with open('./QQAI2/qqai2/plugins/data/command.json', 'w', encoding="UTF-8") as command:
        command_data = {'普通功能': {'签到': ['签到', 'qd'],
                        '抽签': ['抽签', 'cq'],
                        '解签': ['解签', 'jq'],
                        '存签': ['存签', 'CQ'],
                        '上货': ['上货'],
                        '下架': ['下架'],
                        '购买': ['购买'],
                        '欢迎语添加': ['welcomeadd', '欢迎语添加'],
                        '欢迎语删除': ['welcomremove','欢迎语删除'],
                        '离别语添加': ['Farewelladd','离别语添加'],
                        '离别语删除': ['Farewellremove','离别语删除'],
                        '点歌': ['点歌', 'music', 'dg'],
                        '音乐下载': ['音乐下载', 'yyxz', 'download_music'],
                        '网站查询': ['web', '查询'],
                        '网站收录': ['入库', 'record'],
                        '随机图片':['随机图片'],
                        'id找图':['id找图'],
                        '气象预报':['天气查询','气象预报','天气预报'],
                        '气象实况':['气象实况'],
                        'help':['菜单','help']},
                        '管理功能': {
                                 '禁言': ['禁言', 'banned_to_post', 'jy'],
                                 '踢出': ['踢出', 'tc', 'kick_out'],
                                 '管理菜单': ['管理菜单', 'admin'],
                                 '开启群禁言': ['开启群禁言', 'on_group_banned_to_post', 'kqqjy'],
                                 '解除群禁言': ['解除群禁言', 'off_group_banned_to_post', 'jcqjy'],
                                 }}
        json.dump(command_data, command, indent=4, ensure_ascii=False)
    with open('./QQAI2/qqai2/plugins/data/command_yml.json', 'w', encoding="UTF-8") as command:
        command_data = {'function': {
                        '签到': 'sing_in',
                        '抽签': 'draw_lots',
                        '解签': 'draw_lots',
                        '存签': 'draw_lots',
                        '点歌': 'music',
                        '上货': 'store',
                        '下架': 'store',
                        '购买': 'store',
                        '音乐下载': 'music',
                        '网站查询': 'web',
                        '网站收录': 'include',
                        '入群欢迎': 'welcome',
                        '退群检测':'farewell',
                        '欢迎语添加':'farewell',
                        '欢迎语删除':'farewell',
                        '离别语添加':'farewell',
                        '离别语删除':'farewell',
                        '随机图片':'picture',
                        'id找图':'picture',
                        '气象预报': 'weather',
                        '气象实况':'weather',
                        'help':'help'},
                        'AdminFunction': {
                        '禁言': 'banned_to_post',
                        '踢出': 'kick_out',
                        '开启群禁言': 'group_banned_to_post',
                        '解除群禁言': 'group_banned_to_post',
                        }}
        json.dump(command_data, command, indent=4, ensure_ascii=False)

        with open('./QQAI2/qqai2/plugins/data/GroupingTesting.json', 'w', encoding="UTF-8") as welcome:
            GroupingTesting = {'welcome': {
                '*': ["你好啊{user},我是本群的群聊机器人小白\n喜欢（唱，跳，rap，篮球）才怪༼ つ ◕_◕ ༽つ\n好了不皮了其实我喜欢你(^///^)祝你在群里聊的开心拜拜ο(=•ω＜=)ρ⌒☆"]
            },
                'Farewell': {
                '*': ['{user}离开了本群让我们为他送行吧ಥ_ಥ']
            }}
            json.dump(GroupingTesting, welcome, indent=4, ensure_ascii=False)
        with open('./QQAI2/qqai2/plugins/data/store.json','w', encoding="UTF-8") as store_content:
            content = {
                '猫粮':{'积分':10,'好感':1},
                '爱心':{'积分':10,'好感':1},
                '糖':{'积分':20,'好感':2},
                '苹果':{'积分':20,'好感':2},
                '蛋糕':{'积分':100,'好感':10},
                '电脑':{'积分':2000,'好感':200}
            }
            json.dump(content, store_content, indent=4, ensure_ascii=False)
        with open('./QQAI2/qqai2/plugins/data/knapsack.json','w',encoding='UTF-8') as knapsack:
            knapsack_content = {

            }
            json.dump(knapsack_content, knapsack, indent=4, ensure_ascii=False)
        # 获取城市代码
        with open('./QQAI2/qqai2/plugins/data/CityCode.json', 'w', encoding="UTF-8") as CityCode:
            url = 'http://www.ip33.com/area_code.html#:~:text=%E4%B8%AD%E5%9B%BD%E7%9C%81%E5%B8%82%E5%8E%BF%E5%9C%B0%E5%8C%BA%E4%BB%A3%E7%A0%81%E4%B8%80%E8%A7%88%E8%A1%A8%20%E7%9B%B8%E5%85%B3%E9%93%BE%E6%8E%A5%EF%BC%9A%20%EF%BC%88%E6%9C%80%E6%96%B0%EF%BC%892019%E5%B9%B4%E4%B8%AD%E5%9B%BD%E7%9C%81%E5%B8%82%E5%8E%BF%E6%95%B0%E6%8D%AE%202018%E5%B9%B4%E4%B8%AD%E5%9B%BD%E7%9C%81%E5%B8%82%E5%8E%BF%E6%95%B0%E6%8D%AE%202017%E5%B9%B4%E4%B8%AD%E5%9B%BD%E7%9C%81%E5%B8%82%E5%8E%BF%E6%95%B0%E6%8D%AE%202016%E5%B9%B4%E4%B8%AD%E5%9B%BD%E7%9C%81%E5%B8%82%E5%8E%BF%E6%95%B0%E6%8D%AE,2015%E5%B9%B4%E4%B8%AD%E5%9B%BD%E7%9C%81%E5%B8%82%E5%8E%BF%E6%95%B0%E6%8D%AE%20%E6%8C%89%E4%B8%8B%E9%94%AE%E7%9B%98%20ctrl%20%2B%20f%20%E5%8F%AF%E5%BF%AB%E9%80%9F%E6%9F%A5%E6%89%BE'
            data = requests.get(url).content.decode('utf-8')
            A = re.findall(re.compile("<h4>(.+)</h4>"), data)
            B = re.findall(re.compile("<h5>(.+)</h5>"), data)
            C = re.findall(re.compile("<li>(.+)</li>"), data)
            province = []  # 省名称
            provincecode = []  # 省代码
            city = []  # 市名称
            citycode = []  # 市代码
            area = []  # 区名称
            areacode = []  # 区代码
            # 将名称与代码分开
            for i in A:
                province.append(i.split(" ")[0])
                provincecode.append(i.split(" ")[1])
            for j in B:
                city.append(j.split(" ")[0])
                citycode.append(j.split(" ")[1])
            for k in C:
                area.append(k.split(" ")[0])
                areacode.append(k.split(" ")[1])
            ProvinceDict = dict(zip(province, provincecode))
            CodeData = {}
            # 将各部分组合为字典
            for h in ProvinceDict:
                CodeData.update({h: {}})
                for z in citycode:
                    if z[0:2] == ProvinceDict[h]:
                        CodeData[h].update({city[citycode.index(z)]: {}})
                        for m in areacode:
                            if m[0:4] == z:
                                CodeData[h][city[citycode.index(z)]].update({area[areacode.index(m)]: m})
            json.dump(CodeData,CityCode, indent=4, ensure_ascii=False)
    print('\033[33m 配置成功！\033[0m')


