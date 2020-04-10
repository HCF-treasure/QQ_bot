from nonebot import on_command,CommandSession
import requests
@on_command('知乎日报',aliases=['知乎'])#后者是取别名
async def _(session):
    url = 'https://news-at.zhihu.com/api/4/news/latest'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Mobile Safari/537.36 SE 2.X MetaSr 1.0'}
    resp = requests.get(url, headers=headers)
    data = resp.json()  # json.loads(resp.text)
    stories = data['stories']
    # data.get('stories')#安全
    STORY_URL = 'https://daily.zhihu.com/story/{}'
    reply = ''
    for story in stories:
        url = STORY_URL.format(story['id'])
        title = story['title']
        # story.get('title','未知内容')
        reply += f'\n{title}\n{url}\n'  # 拼接字符串
    await session.send(reply)