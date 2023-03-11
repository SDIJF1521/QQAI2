import json
import pymysql
import sqlite3
import config.yml_DATA
import config.config_json
def Data(data=None, ReadWrite=None):
    '''

    :param data: sql语句或者json数据默认为空
    :param ReadWrite: json读写选项（w/r）
    :return:
    '''

    if config.yml_DATA.data == 'sqlite':
        conn = sqlite3.connect('./qqai2/plugins/data/data.db')         #连接sqlite数据库
        cursor = conn.cursor()                                         #创建游标对象
        print(data)
        sqldata = cursor.execute(data)
        conn.commit()                                                  #提交
        return sqldata.fetchall()
    if config.yml_DATA.data == 'mysql':
        conn = pymysql.connect(host=str(config.config_json.DataJson()['mysql']['host']),
                               user=config.config_json.DataJson()['mysql']['user'],
                               password=config.config_json.DataJson()['mysql']['password'],
                               database=config.config_json.DataJson()['mysql']['数据库'])
        cursor = conn.cursor()
        cursor.execute(data)
        conn.commit()
        return cursor.fetchall()
    elif config.yml_DATA.data == 'json' and ReadWrite == 'r':
        with open('./qqai2/plugins/data/data.json', 'r',encoding='UTF-8') as f:
            return json.load(f)
    elif config.yml_DATA.data == 'json' and ReadWrite == 'w':
        with open('./qqai2/plugins/data/data.json', 'w', encoding="UTF-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
def GroupingTestingFile(data=None, ReadWrite=None):
    if ReadWrite == 'r':
        with open('./qqai2/plugins/data/GroupingTesting.json', 'r', encoding='UTF-8') as f:
            return json.load(f)
    elif ReadWrite == 'w':
        with open('./qqai2/plugins/data/GroupingTesting.json', 'w', encoding="UTF-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print('OK')
