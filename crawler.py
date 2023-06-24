import requests
import lxml
import json
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
url = "https://www.lizhi.fm/label/24229920835639472/"  ##历史类url


def download(url, name):
    """
    下载函数，参数url和文件名
    :param url:
    :param name:
    :return:
    """
    ##rooturl="https://www.lizhi.fm/hidden_ph/mkVG3dFFa0M"
    f = requests.get(url, headers=headers).json()
    if f != None and f['data'] != None and f['data']['url'] != None:
        dataurl = f['data']['url']
        ##print(f,dataurl)
        if dataurl != None:
            print("开始下载")
            audio = requests.get(dataurl, headers=headers)
            file = open(name, 'ab')  # 文件路径  文件读写方式 a文件追加（不存在新建） b进制文件
            file.write(audio.content)
            file.close()
            print("下载完了")


if __name__ == "__main__":
    """
    下载前两页的audio，因为第一页有5个是付费内容，下载不了
    """
    userurl = "https://www.lizhi.fm/user/897566"  ##历史类分类博主的url，这里我选的是野史煮酒
    lurl = "https://www.lizhi.fm/hidden_ph/"  ##音频文件的url前缀
    soup = BeautifulSoup(requests.get(userurl, headers=headers).content, 'lxml').find_all("a")
    soup1 = BeautifulSoup(requests.get(userurl + "/p/2.html", headers=headers).content, 'lxml').find_all("a")
    ##namelist=[]
    urllist = []
    for i in soup:
        ##namelist.append()
        if i.get("data-hidden-ph") != None:
            urllist.append((lurl + i.get("data-hidden-ph"),
                            re.sub('([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u007a])', '',
                                   i.get("title"))+ ".mp3"))  ##正则表达式去除特殊字符
    for i in soup1:
        ##namelist.append()
        if i.get("data-hidden-ph") != None:
            urllist.append((lurl + i.get("data-hidden-ph"),
                            re.sub('([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u007a])', '',
                                   i.get("title"))+ ".mp3"))  ##正则表达式去除特殊字符
    ##print(urllist)
    for element in urllist:
        download(element[0], element[1])
