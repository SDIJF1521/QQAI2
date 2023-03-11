import re
from nonebot import config
from nonebot import on_regex
from nonebot import get_driver
from QQAI2.qqai2.plugins.content.got import *
from QQAI2.qqai2.plugins.content.web import *
from QQAI2.qqai2.plugins.content.music import *
from QQAI2.qqai2.plugins.content.SingIn import *
from QQAI2.qqai2.plugins.content.welcome import *
from QQAI2.qqai2.plugins.content.analysis import *
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message

allocation = on_regex('.+', priority=5)  # 注册功能调度事件


@allocation.handle()
async def Allocation(event: GroupMessageEvent, bot: Bot):
    #获取机器人所接管的所有群
    groupdata = await bot.get_group_list()
    grouplist = []
    for h in groupdata:
        grouplist.append(str(h['group_id']))
    NewsData = event.get_event_description().replace('\n', '')
    # 获取群内成员发送的消息
    print(NewsData)
    News = re.findall(re.compile("from \d+@\[群:\d+] '(.+)'"), NewsData)
    # 回复式命令响应
    with open('./qqai2/plugins/data/reply.json', 'r') as f:
        JsonData = json.load(f)
    if str(event.group_id) + '|' + str(event.user_id) in JsonData['name']:
        if len(RecordR()['name']) != 0:
            value = got(str(event.group_id) + '|' + str(event.user_id), News[0])
            print(value)
            if 'str' in value:
                msg = f'[CQ:at,qq={str(event.user_id)}]\n{value["str"]}'
                await allocation.send(Message(msg))
            elif 'voice' in value:
                msg = f'[CQ:record,file={value["voice"][0]}]'
                try:
                    await allocation.send(Message(msg))
                except:
                    await allocation.send('小白找不到该歌曲::>_<::')
            elif 'file' in value:
                file = os.getcwd().replace('\\', '/') + '/' + value["file"][2:len(value["file"])]
                print(file)
                try:
                    await bot.call_api('upload_group_file', **{'group_id': event.group_id,
                                                               'file': f'{file}',
                                                               'name': News[0] + '.aac'})
                    os.remove(file)
                except:
                    await bot.call_api('upload_group_file', **{'group_id': event.group_id,
                                                               'file': f'{file}',
                                                               'name': News[0] + '.aac'})
                    os.remove(file)
    else:
        with open('./qqai2/plugins/data/command.json', encoding='UTF-8') as command:  # 提取command。json配置数据
            DataCommand = json.load(command)
            function = DataCommand['普通功能']
            AdminFunction = DataCommand['管理功能']
        with open('./qqai2/plugins/data/command_yml.json',encoding='UTF-8') as js_yml:
            command_yml = json.load(js_yml)


        print(News[0])
        for i in function:
            for j in function[i]:
                if len(News[0]) >= len(j):
                    NewsCommand = News[0][0:len(j)]
                    if NewsCommand in j:
                        print(j + ' 命令匹配成功功能为: ' + i)

                        # 签到事件
                        if NewsCommand in function['签到']:
                            Save = command_yml['function']['签到']
                            if yml_DATA.yml_data['content']['function'][Save]:
                                ReverseBack = sing_in(str(event.group_id) + '|' + str(event.user_id))
                                if isinstance(ReverseBack, list) or isinstance(ReverseBack, tuple):
                                    print(ReverseBack)
                                    out = '[CQ:at,qq=%s]\n签到成功!\n获得积分：%d点\n您当前的积分为：%s 点\n您已签到: %s 天' % (
                                    event.user_id, ReverseBack[1], str(ReverseBack[0][0][1]), str(ReverseBack[0][0][3]))
                                    await allocation.send(Message(out))
                                elif isinstance(ReverseBack, str):
                                    out = '[CQ:at,qq=%s]]%s' % (str(event.user_id), ReverseBack)
                                    await allocation.send(Message(out))
                            else:
                                await allocation.send('该功能为开启如果想使用的话请联系管理')




                        # 存签事件
                        elif NewsCommand in function['存签']:
                            FunctionName = command_yml['function']['存签']
                            if yml_DATA.yml_data['content']['function'][FunctionName]:
                                if len(News[0]) > len(j):
                                    print(AnalysisNews(News=News[0], command=j)[0])
                                    Save = (save(News[0]))
                                    print(Save)
                                    if isinstance(Save, list) or isinstance(Save, tuple):
                                        await allocation.send('小白已将信息存入(✿◕‿◕✿)')
                                    else:
                                        await allocation.send(Save)
                                else:
                                    await allocation.send('请按照 签诗|意思 的形式存入')
                                    RecordW(use=str(event.group_id) + '|' + str(event.user_id), function=i,
                                            time=time.time())
                            else:
                                await allocation.send('该功能为开启如果想使用的话请联系管理')



                        # 抽签事件
                        elif NewsCommand in function['抽签']:
                            FunctionName = command_yml['function']['抽签']
                            if yml_DATA.yml_data['content']['function'][FunctionName]:
                                DL = DrawLots(str(event.group_id) + '|' + str(event.user_id))
                                if isinstance(DL, str):
                                    out = '[CQ:at,qq=' + str(event.user_id) + ']' + DL
                                    await allocation.send(Message(out))
                                elif isinstance(DL, list) or isinstance(DL, tuple):
                                    msg = '[CQ:at,qq=' + str(event.user_id) + ']\n您抽中小白签库第' + str(
                                        DL[0][0]) + '签\n签诗：' + str(DL[0][1])
                                    await allocation.send(Message(msg))
                            else:
                                await allocation.send('该功能为开启如果想使用的话请联系管理')


                        # 解签事件
                        elif NewsCommand in function['解签']:
                            FunctionName = command_yml['function']['解签']
                            if yml_DATA.yml_data['content']['function'][FunctionName]:
                                Inted = intend(str(event.group_id) + '|' + str(event.user_id))
                                if isinstance(Inted, str):
                                    out = '[CQ:at,qq=' + str(event.user_id) + ']' + Inted
                                    await allocation.send(Message(out))
                            else:
                                await allocation.send('该功能为开启如果想使用的话请联系管理')


                        # 点歌事件
                        elif NewsCommand in function['点歌']:
                            FunctionName = command_yml['function']['点歌']
                            if yml_DATA.yml_data['content']['function'][FunctionName]:
                                if len(config.yml_DATA.music_API) != 0:
                                    try:
                                        print(requests.get(config.yml_DATA.music_API).status_code)
                                        if requests.get(config.yml_DATA.music_API).status_code == 200:
                                            print('ok')
                                            if len(News[0]) > len(j):
                                                data = str(News[0][2:len(News[0])]).replace(' ', '')
                                                MusicUrl = music(data)
                                                print(MusicUrl)
                                                msg = f'[CQ:record,file={MusicUrl[0]}]'
                                                print(msg)
                                                try:
                                                    await allocation.send(Message(msg))
                                                except:
                                                    await allocation.send('小白找不到该歌曲::>_<::')
                                            else:
                                                RecordW(use=str(event.group_id) + '|' + str(event.user_id), function=i,
                                                        time=time.time())
                                                await allocation.send('请输入歌名或音乐id:')
                                    except:
                                        await allocation.send('无效API请联系小白的管理进行API的配置{{{(>_<)}}}')
                            else:
                                await allocation.send('该功能为开启如果想使用的话请联系管理')



                        # 音乐下载事件
                        elif NewsCommand in function['音乐下载']:
                            FunctionName = command_yml['function']['音乐下载']
                            if yml_DATA.yml_data['content']['function'][FunctionName]:
                                if len(config.yml_DATA.music_API) != 0:
                                    print(requests.get(config.yml_DATA.music_API).status_code)
                                    if requests.get(config.yml_DATA.music_API).status_code == 200:
                                        try:
                                            if len(News[0]) > len(j):
                                                data = str(News[0][4:len(News[0])]).replace(' ', '')
                                                DATA = MusicDownload(data)
                                                if isinstance(DATA, list):
                                                    file = os.getcwd().replace('\\', '/') + '/' + DATA[0][2:len(
                                                        MusicDownload(data))]
                                                    print(file)
                                                    await bot.call_api('upload_group_file',
                                                                       **{'group_id': event.group_id,
                                                                          'file': f'{file}',
                                                                          'name': data + '.aac'})
                                                    os.remove(file)
                                                else:
                                                    await allocation.send(DATA)

                                            else:
                                                RecordW(use=str(event.group_id) + '|' + str(event.user_id), function=i,
                                                        time=time.time())
                                                await allocation.send('请输入歌名或音乐id:')
                                        except:
                                            await allocation.send('无效API请联系小白的管理进行API的配置{{{(>_<)}}}')
                            else:
                                await allocation.send('该功能为开启如果想使用的话请联系管理')


                        # 网站存入
                        elif NewsCommand in function['网站收录']:
                            FunctionName = command_yml['function']['网站收录']
                            if yml_DATA.yml_data['content']['function'][FunctionName]:
                                if len(News[0]) > len(j):
                                    data = deposit(News[0], j)
                                    print(data)
                                    if isinstance(data, str):
                                        msg = f'[CQ:at,qq={str(event.user_id)}]\n{data}'
                                        await allocation.send(msg)
                                else:
                                    RecordW(use=str(event.group_id) + '|' + str(event.user_id), function=i,
                                            time=time.time())
                                    await allocation.send('请按 网站名称|网址 方式写入')
                            else:
                                await allocation.send('该功能为开启如果想使用的话请联系管理')


                        # 网站查询
                        elif NewsCommand in function['网站查询']:
                            FunctionName = command_yml['function']['网站查询']
                            if yml_DATA.yml_data['content']['function'][FunctionName]:
                                if len(News[0]) > len(j):
                                    data = web(News[0], j)
                                    print(data)
                                    if isinstance(data, str):
                                        msg = f'[CQ:at,qq={str(event.user_id)}]\n{data}'
                                        await allocation.send(Message(msg))
                                else:
                                    RecordW(use=str(event.group_id) + '|' + str(event.user_id), function=i,
                                            time=time.time())
                                    await allocation.send('请输入要查询的网站名称：')
                            else:
                                await allocation.send('该功能为开启如果想使用的话请联系管理')

                        # 欢迎语添加
                        elif NewsCommand in function['欢迎语添加']:
                            FunctionName = command_yml['function']['欢迎语添加']
                            if yml_DATA.yml_data['content']['function'][FunctionName]:
                                if len(News[0]) > len(j):
                                    if str(event.user_id) in get_driver().config.superusers:
                                        print('ok')
                                        WelcomeData = AnalysisNews(News=News[0], command=j, division=False)
                                        if '|' in News[0]:
                                            welcomedata = AnalysisNews(News=News[0], command=j, symbol='|', ManyTimes=False)     # 群号与欢迎语参数分离
                                            print(welcomedata)
                                            if welcomedata[0] in grouplist:
                                                welcome_add(GroupNumber=welcomedata[0], WelcomeAdd=welcomedata[1], whole=False)