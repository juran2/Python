import requests
import threading
from bs4 import BeautifulSoup
from queue import Queue


def get_html(per):
    name_url='http://588ku.com/sucai/0-pxnum-0-%s-0-0-2/' % (per)
    r=requests.get(name_url)
    s=BeautifulSoup(r.content,'html.parser')

class threadDownload(threading.Thread):
    def __init__(self,que,no):
        threading.Thread.__init__(self)
        self.que=que
        self.no=no
    def run(self):
        while True:
            if not self.que.empty():
                save_img(self.que.get()[0])
            else:
                break
def get_img_html(html1):
    y=[]
    soup=BeautifulSoup()

    return y

def get_img(html2):
    for a in range(0,5):
        thredD=threadDownload(out_queue,a)
        thredD.start()

x=1
def save_img(img_url):
    global x
    x+=1
    img_url1 =img_url.split('=')[-1][1:-2].replace('jp','jpg').replace('pn','png').replace('gi','gif')
    print u'正在下载'+'http:'+img_url1
    img_content=requests.get('http:'+img_url1).content
    with open('doutu/%s.jpg'% x,'wb') as f:
        f.write(img_content)


#主函数
def main():
    start_url='https://www.doutula.com/article/list/?page='
    for j in range(1,5):
        start_html=get_html(start_url+str(j))
        b=get_img_html(start_html)
        for i in b:
            get_img(i)
if __name__=='__main__':
    main()



