from nonebot.adapters.onebot.v11 import Bot
from nonebot import on_command
import json
S = on_command('hq', aliases={'获取'}, priority=1)
@S.handle()
async def A(bot: Bot):
    print('ok')
    A = await bot.get_group_list()
    print(A)