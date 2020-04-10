from nonebot import on_command,CommandSession,on_request,RequestSession
from nonebot import permission as perm
import urllib.parse


@on_command('看电影',aliases=['搜电影'],permission=perm.GROUP)#后者是取别名
async def _(session):
    msg = session.ctx['raw_message']
    cmd,a,word = msg.split(' ', maxsplit=2)
    keyword = urllib.parse.urlencode({"wd": word})
    url1 = f'https://www.adcmove.com/search/-------------.html?{keyword}'
    url2 = f'https://www.kkk8.tv/vod/search.html?{keyword}&submit='
    keyword = urllib.parse.urlencode({"key": word})
    url3 = f'https://neets.cc/search?{keyword}'
    keyword = urllib.parse.urlencode({"q": word})
    url4 = f'https://gaoqing.fm/s.php?{keyword}'
    reply = f'关于{word}的搜索结果如下：\n渠道一：{url1}\n渠道二：{url2}\n渠道三：{url3}\n渠道四：\n{url4}\n祝您观影愉快~~'
    await session.send(reply)

@on_command('电影',aliases=['视频'])#可以换成群主，群管理
async def _(session:CommandSession):
    msg = session.ctx['raw_message']
    cmd,word = msg.split(' ', maxsplit=1)
    keyword = urllib.parse.urlencode({"wd": word})
    url1 = f'https://www.adcmove.com/search/-------------.html?{keyword}'
    url2 = f'https://www.kkk8.tv/vod/search.html?{keyword}&submit='
    keyword = urllib.parse.urlencode({"key": word})
    url3 = f'https://neets.cc/search?{keyword}'
    keyword = urllib.parse.urlencode({"q": word})
    url4 = f'https://gaoqing.fm/s.php?{keyword}'
    reply = f'关于{word}的搜索结果如下：\n渠道一：{url1}\n渠道二：{url2}\n渠道三：{url3}\n渠道四：\n{url4}\n祝您观影愉快~~'
    await session.send(reply)