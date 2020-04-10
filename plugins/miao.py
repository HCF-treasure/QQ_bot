from nonebot import on_command,CommandSession,on_request,RequestSession
from nonebot import permission as perm
from nonebot import CQHttpError
#@on_command里面有很多参数
@on_command('喵一个',aliases=['miao','喵喵','喵'])#后者是取别名
async def _(session):
    print('测试结果',session.ctx['sender'])
    await session.send('喵~~~！')

#获取群的总人数
@on_command('get_member_count',aliases=['总人数'],permission=perm.GROUP_ADMIN)#可以换成群主，群管理
async def _(session:CommandSession):
    group_id = session.ctx['group_id']
    try:
        member_list = await session.bot.get_group_member_list(group_id=group_id)#获取群员id
    except CQHttpError:
        await session.send('无法获取')
        return#这样可以直接避免报错
    await session.send(f'群里一共有{len(member_list)}个人')

@on_request('friend')#同意好友请求
async def _(session:RequestSession):
    await session.approve()
    #await session.reject()
