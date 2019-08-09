import os
import sys
import requests
from bs4 import BeautifulSoup

def get_proxy():
    r = requests.get("http://127.0.0.1:5555/random")
    proxy = BeautifulSoup(r.text,"lxml").get_text()
    return proxy

def crawl(url, proxy):
    proxies = {'http': proxy}
    r = requests.get(url, proxies = proxies)
    return r.text

def main():
    proxy = get_proxy()
    print("成功获取代理",proxy)
    html = crawl("http://docs.jinkan.org/docs/flask/", proxy)
    print(html)

if __name__ == '__main__':
    main()
