import time
from QQAI2.qqai2.plugins.content.draw import *
from QQAI2.qqai2.plugins.content.web import *
from QQAI2.qqai2.plugins.content.music import *
def got(use,data):
    if use in RecordR()['name']:
        indexes = RecordR()['name'].index(use)
        if RecordR()['time'][RecordR()['name'].index(use)]+60 > time.time():
            if RecordR()['function'][indexes] == '存签':
                Save = save(data)
                RecordV(use)
                if isinstance(Save, list):
                    return {'str': '小白已将信息存入(✿◕‿◕✿)'}
                else:
                    return {'str': Save}
            elif RecordR()['function'][indexes] == '点歌':
                MusicUrl=music(data)
                RecordV(use)
                return {'voice':MusicUrl}
            elif RecordR()['function'][indexes] == '音乐下载':
                data = MusicDownload(data)
                RecordV(use)
                return {'file': data}
            elif RecordR()['function'][indexes] == '网站收录':
                data = deposit(data)
                RecordV(use)
                return {'str': data}
            elif RecordR()['function'][indexes] == '网站查询':
                data = web(data)
                print({'str': data})
                RecordV(use)

                return {'str': data}
        else:
            if RecordR()['time'][RecordR()['name'].index(use)]+20 <= time.time():
                RecordV(use)