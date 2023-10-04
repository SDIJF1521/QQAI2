from pathlib import Path
from nonebot.rule import to_me
from revChatGPT.V1 import Chatbot
from nonebot.adapters import Event
from abc import ABC, abstractmethod
from QQAI2.qqai2.plugins.content.got import *
from QQAI2.qqai2.plugins.content.web import *
from QQAI2.qqai2.plugins.content.store import *
from QQAI2.qqai2.plugins.content.music import *
from QQAI2.qqai2.plugins.content.SingIn import *
from QQAI2.qqai2.plugins.content.picture import *
from QQAI2.qqai2.plugins.content.weather import *
from QQAI2.qqai2.plugins.content.welcome import *
from QQAI2.qqai2.plugins.content.analysis import *
from nonebot import get_driver,on_regex,on_notice,on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message,GroupIncreaseNoticeEvent,GroupDecreaseNoticeEvent,PokeNotifyEvent,MessageSegment



# 定义参数类
'''
关键参数提取类
'''
class Parameter:
    def __init__(self,Command:str,Parameter:str,News:str):
        """

        :param Command: 命令
        :param Parameter: 功能名称
        :param News: 聊天信息
        """
        with open('./qqai2/plugins/data/command_yml.json', encoding='UTF-8') as js_yml:
            command_yml = json.load(js_yml)
        Save = command_yml['function'][Parameter]      #通过映射文件找到对应配置项
        ContainParameter = False
        if len(News) > len(Command):
            ContainParameter = True
            Information ={'天气查询':AnalysisNews(News=News,command=Command,division=False,ManyTimes=False),
                          '语言':{'A':AnalysisNews(News=News, command=Command, symbol='|', ManyTimes=False),
                                 'B':AnalysisNews(News=News, command=Command, division=False)},
                          'id找图':AnalysisNews(News=News,command=Command,division=False),
                          '上货':AnalysisNews(News=News,command=Command),
                          '下架':AnalysisNews(News=News, command=Command,division=False,ManyTimes=False),
                          '购买':AnalysisNews(News=News,command=Command),
                          '点歌':str(News[2:len(News)]).replace(' ', ''),
                          '音乐下载':str(News[4:len(News)]).replace(' ', '')
                          }
            self.Information = Information
        self.ContainParameter = ContainParameter    #是否含参判定变量
        self.Save = Save

# 定义策略接口
class StrategyPort(ABC):
    @abstractmethod
    def Execute(self,User:str,Group:str,**Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        pass


# 签到功能实现类
class SignIn(StrategyPort):
    def Execute(self,User:str,Group:str,**Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        if Arguments['Arguments']['FunctionSwitch']:
            ReverseBack = sing_in(str(User) + '|' + str(Group))
            if isinstance(ReverseBack, list) or isinstance(ReverseBack, tuple):
                out = '[CQ:at,qq=%s]\n签到成功!\n获得积分：%d点\n您当前的积分为：%s 点\n您已签到: %s 天' % (
                    User, ReverseBack[1], str(ReverseBack[0][0][1]), str(ReverseBack[0][0][3]))
                return out
            elif isinstance(ReverseBack, str):
                out = '[CQ:at,qq=%s]]%s' % (str(User), ReverseBack)
                return out
        else:
            return '该功能为开启如果想使用的话请联系管理'


#存签功能实现类
class Deposit(StrategyPort):
    def Execute(self, User: str, Group: str, **Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        if Arguments['Arguments']['FunctionSwitch']:
            if Arguments['Arguments']['ContainParameter']:
                Save = (Arguments['Arguments']['News'])
                # print(Save)
                if isinstance(Save, list) or isinstance(Save, tuple):
                    return '小白已将信息存入(✿◕‿◕✿)'
                else:
                    return Save
            else:
                RecordW(use=str(Group) + '|' + str(User), function=Arguments['Arguments']['FunctionName'],
                        time=time.time())
                return '请按照 签诗|意思 的形式存入'


# 抽签功能实现类
class DrawLots(StrategyPort):
    def Execute(self,User:str,Group:str,**Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        if Arguments['Arguments']['FunctionSwitch']:
            pass


# 解签功能实现类
class DrawIntend(StrategyPort):
    def Execute(self,User:str,Group:str,**Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        if Arguments['Arguments']['FunctionSwitch']:
            pass


# 网站收录功能实现类
class WebDeposit(StrategyPort):
    def Execute(self,User:str,Group:str,**Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        if Arguments['Arguments']['FunctionSwitch']:
            if Arguments['Arguments']['ContainParameter']:
                data = deposit(Arguments['Arguments']['Content'], Arguments['Arguments']['FunctionName'])
                # print(data)
                if isinstance(data, str):
                    msg = f'[CQ:at,qq={str(User)}]\n{data}'
                    return msg
            else:
                RecordW(use=str(Group) + '|' + str(User), function=Arguments['Arguments']['FunctionName'],
                        time=time.time())
                return '请按 网站名称|网址 方式写入'
        else:
            return '该功能为开启如果想使用的话请联系管理'




#网站查询类
class WebInquiry(StrategyPort):
    def Execute(self,User:str,Group:str,**Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        if Arguments['Arguments']['FunctionSwitch']:
            if Arguments['Arguments']['ContainParameter']:
                print(Arguments)
                data = web(Arguments['Arguments']['Content'], Arguments['Arguments']['FunctionName'])
                if isinstance(data, str):
                    msg = f'[CQ:at,qq={str(User)}]\n{data}'
                    return msg
                else:
                    return '程序异常终止'
            else:
                RecordW(use=str(Group) + '|' + str(User), function= Arguments['Arguments']['FunctionName'],
                        time=time.time())
                return '请输入要查询的网站名称：'
        else:
            return '该功能为开启如果想使用的话请联系管理'


# 点歌功能实现类
class Music(StrategyPort):
    def Execute(self,User:str,Group:str,**Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        if Arguments['Arguments']['FunctionSwitch']:
            pass


#上下文类
class Context:
    def __init__(self,Strategy):
        self.Strategy = Strategy
    def execute_strategy(self,User:str,Group:str,Parameter:str,**Arguments):
        """

        :param User: 用户名
        :param Group: 群号
        :param Parameter: 功能名称
        :param Arguments: 功能函数所需信息传入接口
        :return:
        """
        print(self.Strategy)
        return self.Strategy[Parameter].Execute(User, Group, **Arguments)








allocation = on_regex('.+', priority=5)  # 注册功能调度事件
notice=on_notice(priority=5)
gpt = on_regex('.+',priority=3,rule=to_me())
gpt_command = on_command('小白',priority=4)
gpt_user = []   # 使用人员列表用于避免功能冲突
@allocation.handle()
async def Allocation(event: GroupMessageEvent, bot: Bot,event1:Event):
    # 普通用户使用功能
    SchemeA = Context({'签到': SignIn(),
                       '抽签': DrawLots(),
                       '解签': DrawIntend(),
                       '点歌':Music(),
                       '网站收录':WebDeposit(),
                       '网站查询':WebInquiry()})
    #管理使用功能
    SchemeB = Context({'签到': SignIn(),
                       '存签': Deposit(),
                       '抽签': DrawLots(),
                       '解签': DrawIntend(),
                       '点歌': Music(),
                       '网站收录': WebDeposit(),
                       '网站查询': WebInquiry()})

    News = str(event.message)       #获取用户聊天信息
    # 获取发送者权限
    get_group_member_info = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
    # 获取机器人所接管的所有群
    groupdata = await bot.get_group_list()
    grouplist = []
    for h in groupdata:
        grouplist.append(str(h['group_id']))
    News = str(event.message)
    # 获取群内成员发送的消息
    print(News)
    # 回复式命令响应
    with open('./qqai2/plugins/data/reply.json', 'r', encoding="UTF-8") as f:
        JsonData = json.load(f)
    if str(event.group_id) + '|' + str(event.user_id) in JsonData['name']:
        if len(RecordR()['name']) != 0:
            value = got(user=str(event.group_id) + '|' + str(event.user_id), data=News,
                        power=get_group_member_info['role'], GroupNumber=str(event.group_id),
                        admin=get_driver().config.superusers, grouplist=grouplist)
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
                try:
                    await bot.call_api('upload_group_file', **{'group_id': event.group_id,
                                                               'file': f'{file}',
                                                               'name': News + '.aac'})
                    os.remove(file)
                except:
                    await bot.call_api('upload_group_file', **{'group_id': event.group_id,
                                                               'file': f'{file}',
                                                               'name': News + '.aac'})
                    os.remove(file)
            elif 'image' in value:
                file = os.getcwd().replace('\\', '/') + '/' + value["image"]  # 获取图像路径
                try:
                    await allocation.send(Message(MessageSegment.image(Path(file))))
                    os.remove(file)
                except:
                    await allocation.send(Message(MessageSegment.image(Path(file))))
                    os.remove(file)
    else:
        with open('./qqai2/plugins/data/reply.json', 'r', encoding="UTF-8") as f:
            JsonData = json.load(f)
        if not str(event.group_id) + '|' + str(event.user_id) in JsonData['name']:
            with open('./qqai2/plugins/data/command.json', encoding='UTF-8') as command:  # 提取command。json配置数据
                DataCommand = json.load(command)
                function = DataCommand['普通功能']
                AdminFunction = DataCommand['管理功能']
            for i in function:
                for j in function[i]:
                    parameter = Parameter(Command=j, Parameter=i, News=News)
                    if len(News) >= len(j):     #判断是否为命令
                        if News[0:len(j)] in j:
                            print(j + ' 命令匹配成功功能为: ' + i)
                            if str(event.user_id) in get_driver().config.superusers:
                                await allocation.send(Message(SchemeB.execute_strategy(
                                    User=str(event.user_id),Group=str(event.group_id),Parameter=i,Arguments={
                                        'FunctionSwitch':yml_DATA.yml_data['content']['function'][parameter.Save],
                                        'ContainParameter': parameter.ContainParameter,
                                        'Content': News,
                                        'FunctionName':i
                                    })))
                            else:
                                print(1)
                                await allocation.send(Message(SchemeB.execute_strategy(
                                    User=str(event.user_id),Group=str(event.group_id),Parameter=i,Arguments={
                                        'FunctionSwitch':yml_DATA.yml_data['content']['function'][parameter.Save],
                                        'ContainParameter': parameter.ContainParameter,
                                        'Content': News,
                                        'FunctionName':i
                                    })))

# @形式触发gpt
@gpt.handle()
async def chatGPT(event:GroupMessageEvent):
    try:
        if GPT:
            gpt_user.append(str(event.group_id) + '|' + str(event.user_id))
            if len(str(event.message))!=0:
                chatbot = Chatbot(config={
                    "access_token":GPT_access_token},
                    conversation_id=GPT_convo_id)
                prompt = '小白'+str(event.message)
                response = ""

                for data in chatbot.ask(
                        prompt
                ):
                    response = data["message"]
                await gpt.send(Message(response))
            gpt_user.remove(str(event.group_id) + '|' + str(event.user_id))
    except:
        await gpt.send('小白出错了{{{(>_<)}}}请重试！')

# 命令形式触发got
@gpt_command.handle()
async def chatGPT(event:GroupMessageEvent):
    if not str(event.group_id) + '|' + str(event.user_id) in gpt_user:
        if GPT:
            try:
                gpt_user.append(str(event.group_id) + '|' + str(event.user_id))
                if len(str(event.message))!=0:
                    chatbot = Chatbot(config={
                        "access_token":GPT_access_token},
                        conversation_id=GPT_convo_id)

                    prompt = '小白'+str(event.message)
                    response = ""

                    for data in chatbot.ask(
                            prompt
                    ):
                        response = data["message"]
                    await gpt.send(Message(response))
                gpt_user.remove(str(event.group_id) + '|' + str(event.user_id))
            except:
                await gpt_command.send('小白出错了{{{(>_<)}}}请重试！')

#消息事件
@notice.handle()
#入群欢迎
async def greet(event: GroupIncreaseNoticeEvent):
    # 读取配置
    with open('./qqai2/plugins/data/command_yml.json', encoding='UTF-8') as js_yml:
        command_yml = json.load(js_yml)
        FunctionName = command_yml['function']['入群欢迎']
    # 进群欢迎是否启用
    if yml_DATA.yml_data['content']['function'][FunctionName]:
        user = str(event.user_id)
        template = use(GroupNumber=str(event.group_id))
        welcome_language = template
        if '{user}' in template:
            welcome_language = template.replace('{user}',f'[CQ:at,qq={user}]')
        await notice.finish(Message(welcome_language))

# 退群检测
@notice.handle()
async def greet1(event: GroupDecreaseNoticeEvent):
    with open('./qqai2/plugins/data/command_yml.json', encoding='UTF-8') as js_yml:
        command_yml = json.load(js_yml)
        FunctionName = command_yml['function']['退群检测']
    # 进群欢迎是否启用
    if yml_DATA.yml_data['content']['function'][FunctionName]:
        print('ok')
        user = str(event.user_id)
        template = use(GroupNumber=str(event.group_id),greet=False)
        welcome_language = template
        if '{user}' in template:
            welcome_language = template.replace('{user}', f'[CQ:at,qq={user}]')
        await notice.finish(Message(welcome_language))

#彩蛋
@notice.handle()
async def Easter_Egg(event:PokeNotifyEvent,bot:Bot):
    ID = await bot.call_api('get_login_info')
    if event.target_id == ID['user_id']:
      await notice.send(Message('你不要在光天化日之下在这里戳我啊，哒咩!\n[CQ:image,file=b2566dfb4c8c7ef494a7e285161a0080.image,subType=1,url=https://gchat.qpic.cn/gchatpic_new/839682307/760705385-3101003974-B2566DFB4C8C7EF494A7E285161A0080/0?term=2&amp;is_origin=0]'))