import re
import json
import sqlite3
import os
import pymysql
def file(PORT,HOST = '127.0.0.1', name='XB', admin='12345678'):                                 #yml配置执行函数
    with open('./QQAI2/.env.prod', 'r', encoding='utf-8') as env1:
        data = env1.read()
        print(data)
        data_port = re.sub(re.findall(re.compile('PORT=(\d+)'), data)[0], str(PORT), data)
        data_name = re.sub(re.findall(re.compile('NICKNAME=\["(\w+)"'), data_port)[0], name, data_port)
        data = re.sub(re.findall(re.compile('SUPERUSERS=\["(\d+)"'), data_name)[0], admin,data_name)
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
        with open('./config.json', 'r') as config_js:
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
                'admin': {
                    'admin': []
                },
                'word': {
                    'wordlist': []
                },
            'sgin': {
                'id': [],
                '签诗': [],
                '解签': []
            }}
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
                        '欢迎语添加': ['welcomeadd', '欢迎语添加'],
                        '点歌': ['点歌', 'music', 'dg'],
                        '音乐下载': ['音乐下载', 'yyxz', 'download_music'],
                        '帮助': ['帮助', 'help'],
                        '网站查询': ['web', '查询'],
                        '网站收录': ['入库', 'record']},
                        '管理功能': {'管理菜单': ['管理菜单', 'admin'],
                                 '开启群禁言': ['开启群禁言', 'on_group_banned_to_post', 'kqqjy'],
                                 '解除群禁言': ['解除群禁言', 'off_group_banned_to_post', 'jcqjy'],
                                 '禁言': ['禁言', 'banned_to_post', 'jy'],
                                 '踢出': ['踢出', 'tc', 'kick_out']}}
        json.dump(command_data, command, indent=4, ensure_ascii=False)
    with open('./QQAI2/qqai2/plugins/data/command_yml.json', 'w', encoding="UTF-8") as command:
        command_data = {'function': {
                        '签到': 'sing_in',
                        '抽签': 'draw_lots',
                        '解签': 'draw_lots',
                        '存签': 'draw_lots',
                        '点歌': 'music',
                        '音乐下载': 'music',
                        '帮助': 'help',
                        '网站查询': 'web',
                        '网站收录': 'include',
                        '欢迎语添加': 'welcome'},
                        'AdminFunction': {
                        '开启群禁言': 'group_banned_to_post',
                        '解除群禁言': 'group_banned_to_post',
                        '禁言': 'banned_to_post',
                        '踢出': 'kick_out'}}
        json.dump(command_data, command, indent=4, ensure_ascii=False)

        with open('./QQAI2/qqai2/plugins/data/GroupingTesting.json', 'w', encoding="UTF-8") as welcome:
            GroupingTesting = {'welcome': {
                '*': ["你好啊user,我是本群的群聊机器人小白\n喜欢（唱，跳，rap，篮球）才怪༼ つ ◕_◕ ༽つ\n好了皮了其实我喜欢你(^///^)祝你在群里聊的开心拜拜ο(=•ω＜=)ρ⌒☆"]
            },
                'Farewell': {
                '*': ['user离开了本群让我们为他送行吧ಥ_ಥ']
            }}
            json.dump(GroupingTesting, welcome, indent=4, ensure_ascii=False)
    print('\033[33m 配置成功！\033[0m')
