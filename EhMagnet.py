import requests
from bs4 import BeautifulSoup
import time
import os
import threading

# 这个只能爬有种子的画集,没种子的自求多福慢慢下吧
# 打开收藏有绿色

header={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
'Cookie':'THIS IS YOUR COOKIE'
}

def getPage(url,header,page=0):
    while 1:
        try:
            ret = requests.get(url+'?page='+str(page),headers=header)
            ret.encoding = ret.apparent_encoding
            if ret.status_code != 200:
                time.sleep(0.3)
            else:
                return ret
        except:
            time.sleep(0.3)

def getList(header,i):
    subRes = getPage('https://exhentai.org/favorites.php',header,i)
    subSoup = BeautifulSoup(subRes.text,'lxml')
    findArrary = subSoup.find_all(title="Show torrents")
    for r in findArrary:
        getMagnet(r.parent['href'],header)

def getMagnet(url,header):
    while 1:
        try:
            ret = requests.get(url,headers=header)
            if ret.status_code != 200:
                time.sleep(0.3)
            else:
                soup = BeautifulSoup(ret.text,'lxml')
                link = soup.form.a
                print('magnet:?xt=urn:btih:'+os.path.splitext(os.path.basename(link['href']))[0].upper()+"\t"+link.text)
                return
        except:
            time.sleep(0.3)

res = getPage('https://exhentai.org/favorites.php',header)
soup = BeautifulSoup(res.text,'lxml')
page = int(soup.find(class_="ptt").find_all('a')[-2].text)
print("Page:"+str(page))

for i in range(0,page):
    threading.Thread(target=getList,args=(header,i,)).start()