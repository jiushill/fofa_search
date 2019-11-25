#@author:九世
#@time:2019/10/27
#@file:query.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from colorama import init,Fore
from bs4 import BeautifulSoup
import requests
import asyncio
import config
import time
import gevent

init(wrap=True)

banner='''
 ________ ________  ________ ________     
|\  _____\\   __  \|\  _____\\   __  \    
\ \  \__/\ \  \|\  \ \  \__/\ \  \|\  \   
 \ \   __\\ \  \\\  \ \   __\\ \   __  \  
  \ \  \_| \ \  \\\  \ \  \_| \ \  \ \  \\ 
   \ \__\   \ \_______\ \__\   \ \__\ \__\\
    \|__|    \|_______|\|__|    \|__|\|__|

'''

class Fofa(object):
    def __init__(self):
        self.search=config.SEARCH
        self.page=config.PAGE
        self.cookie={}
        for x in config.COOKIES.split(";"):
            key,value=str(x).split('=',1)
            self.cookie[key]=value

        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.calc=0
        self.calc2=0
        self.djcs=[]
        self.xcs=[]
        self.ybs=[]
        self.datas=''
        self.set=0

    def searchs(self,url):
        if self.set==1:
            time.sleep(10)
            self.set=0

        try:
            rqt=requests.get(url=url,headers=self.headers,cookies=self.cookie)
            if 'Retry later' in rqt.text:
                print(Fore.YELLOW+'[!] '+Fore.WHITE+'爬的太快了,出现查询频繁的关键字:{}'.format('Retry later'))
                self.set=1
                self.searchs(url)
            else:
                self.datas+=rqt.text

        except Exception as r:
            print(Fore.RED+'[-] '+Fore.WHITE+'Error:{}'.format(r))

    def djc(self):
        for u in self.ybs:
            if self.calc2==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc2=0
                self.djcs.clear()

            self.djcs.append(u)
            self.calc2+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.calc2 = 0
            self.djcs.clear()

    def xc(self,rw):
        for r in rw:
            self.xcs.append(gevent.spawn(self.searchs,r))

        gevent.joinall(self.xcs)
        b=BeautifulSoup(self.datas,'html.parser')
        for div in b.find_all('div',class_='list_mod_t'):
            b=BeautifulSoup(str(div),'html.parser')
            for href in b.find_all('a',target='_blank'):
                print(href.get('href'))
                print(href.get('href'),file=open('save.txt','a',encoding='utf-8'))

        self.datas=''

    async def get_url(self):
        for page in range(1,self.page+1):
            urls='https://fofa.so/result?page={}&qbase64={}'.format(page,self.search)
            if self.calc==100:
                self.djc()
                self.calc=0
                self.ybs.clear()

            self.calc+=1
            self.ybs.append(urls)

        if len(self.ybs)>0:
            self.djc()
            self.calc = 0
            self.ybs.clear()

if __name__ == '__main__':
    print(banner)
    print(Fore.GREEN+'[FOFA] '+Fore.WHITE+'FOFA变态版-开始工作')
    obj=Fofa()
    loop=asyncio.get_event_loop()
    tg=loop.create_task(obj.get_url())
    loop.run_until_complete(tg)
