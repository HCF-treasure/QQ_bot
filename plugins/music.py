from nonebot import on_command,CommandSession
import urllib.request
import chardet
import re
import urllib.parse
from lxml import etree

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html


def html_code(html):
    encode = chardet.detect(html)['encoding']  # 检测编码格式
    if encode == 'GB2312':
        encode = 'GBK'
    html = html.decode(encode, 'ignore')
    return html


#keyword = urllib.parse.urlencode({"key": '跨时代'})  # 将关键词编码
def get_url(word):
    data = {
        'ct': '24',
        'qqmusic_ver': '1298',
        'new_json': '1',
        'remoteplace': 'txt.yqq.song',
        'searchid': '71746174584266098',
        't': '0',
        'aggr': '1',
        'cr': '1',
        'catZhida': '1',
        'lossless': '0',
        'flag_qc': '0',
        'p': '1',
        'n': '10',
        'w': word,
        'g_tk_new_20200303': '5381',
        'g_tk': '5381',
        'loginUin': '2350904752',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0'
    }
    urllist = []
    keyword = urllib.parse.urlencode(data)  # 将关键词编码
    url1 = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?%s' % keyword
    html = url_open(url1)
    html = str(html)  # 里面有部分不是字符串格式
    print('获取file网页:', url1)
    print('\n搜索链接：')
    pattern = r'"songMID".{17}'
    pattern1 = r'"lyric_hilight":"","mid":".{14}'
    b = re.findall(pattern1, html)
    a = re.findall(pattern, html)
    for i in b:
        url = 'https://y.qq.com/n/yqq/song/%s.html' % i[-14:]
        urllist.append(url)
    for each in a:
        url = 'https://y.qq.com/n/yqq/song/%s.html' % each[11:-1]
        urllist.append(url)
    return urllist


def get_albummid(url):  # 获取该歌曲专辑id
    html = url_open(url)
    html = html_code(html)
    #    print(html)
    #    H = etree.HTML(html)#标准化，初始化,之后使用xpath提取数据
    a = html.find('albummid') + 11
    b = a + 14
    album = html[a:b]
    html = etree.HTML(html)
    global mname
    global msinger
    mname = html.xpath('//h1[@class="data__name_txt"]/text()')
    msinger = html.xpath('//div[@class="data__singer"]/a/text()')

    #    print(html)
    return album


def pid_1(albummid):  # 获得pid
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=albuminfoCallback&g_tk=469196449&loginUin=2350904752&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"comm":{"ct":24,"cv":10000},"albumDetail":{"module":"music.musichallAlbum.AlbumInfoServer","method":"GetAlbumDetail","param":{"albumMid":"%s"}}}' % albummid
    html = url_open(url)
    html = html_code(html)
    b = html.find('}]}}}}') - 1
    a = b - 16
    html = html[a:b]
    return html


def vkey(pid, songmid):
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey%s&g_tk=469196449&loginUin=2350904752&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"5651047720","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"5651047720","songmid":["%s"],"songtype":[0],"uin":"2350904752","loginflag":1,"platform":"20"}},"comm":{"uin":2350904752,"format":"json","ct":24,"cv":0}}' % (
    pid, songmid)
    html = url_open(url)
    html = html_code(html)
    #    print(html)
    a = html.find('purl') + 8
    b = html.find('fromtag=66') + 10
    url = 'http://ws.stream.qqmusic.qq.com/'
    url2 = url + html[a:b]
    #    print(url2)
    #    print(html[a:b])
    return url2


def save_m(url):
    filename = mname[0] + ' ' + msinger[0]
    html = url_open(url)
    with open('%s.mp3' % filename, 'wb') as f:
        f.write(html)
    print('%s下载完毕……' % filename)


def main(arg):
    #    urllist = ['https://y.qq.com/n/yqq/song/004LBwRJ2ohY7s.html']
    # musickey = input('请输入歌曲关键字:')
    musickey = arg
    urllist = get_url(musickey)
    i = 0
    while True:
        albummid = get_albummid(urllist[i])  # "003iFCqj1rZ76E"#专辑编码
        songmid = urllist[0][28:42]  # 歌曲编码
        pid = pid_1(albummid)
        url = vkey(pid, songmid)

        if url == 'http://ws.stream.qqmusic.qq.com/':
            i = i + 1
            if i == len(urllist):
                print('搜索%d首歌曲，全部为vip专属' % len(urllist))
                arg = '搜索%d首歌曲，全部为vip专属' % len(urllist)
                break
        else:
            # save_m(url)
            print('音乐链接', url)
            arg = url
            break
    return arg

@on_command('音乐',aliases=['来一首','歌曲','播放'])#后者是取别名
async def _(session):
    msg = session.ctx['raw_message']
    cmd,key = msg.split(' ',maxsplit=1)
    reply = main(key)
    await session.send(reply)