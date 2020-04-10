from nonebot import on_command,CommandSession
from math import *
from nonebot import permission as perm
@on_command('计算',permission=perm.GROUP)#可以换成群主，群管理
async def _(session:CommandSession):
    msg = session.ctx['raw_message']
    name,cmd,arg = msg.split(' ', maxsplit=2)
    arg = arg.strip()  # 去除空格
    result = eval(arg)  # 计算规范的计算表达式
    await session.send(str(result))

@on_command('求值')#后者是取别名
async def _(session):
    msg = session.ctx['raw_message']
    cmd,arg = msg.split(' ', maxsplit=1)
    arg = arg.strip()  # 去除空格
    result = eval(arg)  # 计算规范的计算表达式
    await session.send(str(result))

