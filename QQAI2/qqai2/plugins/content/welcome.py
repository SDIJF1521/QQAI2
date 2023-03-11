from QQAI2.qqai2.plugins.content.data import *
def welcome_add(WelcomeAdd: str, whole: bool = True, GroupNumber: str = ''):
    '''

    :param WelcomeAdd: 欢迎语
    :param whole: 是否为全部默认为True
    :param GroupNumber:群号
    :return:
    '''
    WlcomeData = GroupingTestingFile(ReadWrite='r')     # 获取GroupingTesting.json文件参数
    if whole:
        print(WlcomeData)
        if WelcomeAdd in WlcomeData['welcome']['*']:    # 检测欢迎语是否已存在
            WlcomeData['welcome']['*'].append(WelcomeAdd)
            print(WlcomeData)
            GroupingTestingFile(data=WlcomeData, ReadWrite='w')
            return '成功存入'
        else:
            return '该欢迎语已存在'
    else:
        if GroupNumber in WlcomeData['welcome']:    # 群号存在GroupingTesting.json文件
            if WelcomeAdd in WlcomeData['welcome']['*']:  # 检测欢迎语是否已存在
                WlcomeData['welcome'][GroupNumber].append(WelcomeAdd)
                GroupingTestingFile(data=WlcomeData, ReadWrite='w')
                return '成功存入'
            else:                                  # 对应群在GroupingTesting.json文件在操作
                print('ys')
                if WelcomeAdd in WlcomeData['welcome'][GroupNumber]:
                    return '该欢迎语已存在'
                else:
                    print('yes')
                    WlcomeData['welcome'][GroupNumber].append(WelcomeAdd)
                    print(WlcomeData)
                    GroupingTestingFile(data=WlcomeData, ReadWrite='w')
                    return '成功存入'
        else:                                       # 群号不存在GroupingTesting.json文件
            if not GroupNumber in WlcomeData['welcome']:  # 群号存在GroupingTesting.json文件
                WlcomeData['welcome'].update({GroupNumber:[WelcomeAdd]})
                print(WlcomeData)
                GroupingTestingFile(data=WlcomeData, ReadWrite='w')
                return '成功存入'
            else:
                return '该欢迎语已存在'