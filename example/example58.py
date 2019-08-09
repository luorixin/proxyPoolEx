from bs4 import BeautifulSoup
import requests
import re
import time
import json

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
  'Accept-Encoding': 'gzip, deflate, sdch',
  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}
def get_proxy():
    r = requests.get("http://127.0.0.1:5555/random")
    proxy = BeautifulSoup(r.text, 'lxml').get_text()
    return proxy

def get_links_from(who_sells, proxy):
    urls = []
    proxies = {'http': 'http://'+proxy, 'https': 'https://'+proxy}
    list_view = 'http://bj.58.com/pbdn/pn{}/'.format(str(who_sells))
    print("列表路径", list_view)
    wb_data = requests.get(list_view, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    for link in soup.select('td.t  a.t'):  # 跟上面的方法等价
        print(link)
        urls.append(link.get('href').split('?')[0])
    return urls

def get_classify_url(proxy):
    url58 = 'http://bj.58.com'
    proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
    wb_data = requests.get(url58, proxies = proxies)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    for link in soup.select('span.jumpBusiness a'):
        classify_href = link.get('href')
        print(classify_href)
        classify_url = url58 + classify_href
        print(classify_url)

def get_item_info(who_sells=0):
    proxy = get_proxy()
    urls = get_links_from(who_sells, proxy)
    for url in urls:
        wb_data = requests.get(url, proxy)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        with open('./result58', 'w', encoding='UTF-8') as w:
            w.write(soup.text)
        # print(soup.select('.infocard__container__item__main__text--price'))
        # data = {
        #     'title': soup.title.text,
        #     'price': soup.select('.infocard__container__item__main__text--price')[0].text,
        #     'date' :soup.select('.detail-title__info__text')[0].text,
        #     'cate' :'个人' if who_sells == 0 else '商家',
        # }
        # result = json.dumps(data, ensure_ascii=True, encoding='UTF-8')
        # print(result)

if __name__ == '__main__':
    get_item_info()



