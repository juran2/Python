import requests
from bs4 import BeautifulSoup
import os


def spider(per):   #每一类素材
    name_url='http://588ku.com/sucai/0-pxnum-0-%s-0-0-2/' % (per)
    r=requests.get(name_url)
    s=BeautifulSoup(r.content,'html.parser')
    ul=s.find('ul',attrs={'class': 'clearfix fl'})
    name=ul.find('li',attrs={'class': 'fl on'}).text

    lei_dict={}
    page_dict={}
    for page_num in range(1,100):
        page_url='http://588ku.com/sucai/0-pxnum-0-%s-0-0-'% (per)+str(page_num)    #每一页素材网址
        print('%s ：正在解析第%s页地址...' % (name,page_num))
        r=requests.get(page_url)
        soup = BeautifulSoup(r.content,'html.parser') #把网页内容打开，解析 
        imgs= soup.find_all('img',attrs={'class': 'lazy'})
        img_url_dict={}
        for img in imgs:  #每一个素材
            title=img.get('title')
            final_url=img.get('data-original')
            if("true" in final_url):
                img_url_dict[str(title)]=str(final_url)
                print('%s'%(name)+title,':',final_url)
        page_dict[page_num]=img_url_dict

    lei_dict[str(name)]=page_dict
    return lei_dict


def download(lei):
    for key in lei:
        files_name='E:/qkw2/%s/' % (key)     #一级文件名
        if not os.path.exists(files_name):
            os.makedirs(files_name)
        for key2 in lei[key]:
            files_name2=files_name+'%s/' % (key2)  #二级文件名
            if not os.path.exists(files_name2):
                os.makedirs(files_name2)
            print('%s ：正在下载第%s页图片' % (key,key2))
            for key3 in lei[key][key2]:
                file_name= '%s.jpg' % (key3)
                local_file_name=files_name2+file_name
                download_res=requests.get(lei[key][key2][key3])
                with open(local_file_name,'wb') as f:
                    f.write(download_res.content)
                    f.close()


if __name__ =='__main__':
    class_list=['38','39','40','45','52','53','78']
    temp_url_dict={}
    for per in class_list:
        temp_url_dict=spider(str(per))
        download(temp_url_dict)

