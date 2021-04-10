import scrapy
from bs4 import BeautifulSoup as bs

import requests
import redis


def start_requests():
    urls = ['http://www.xiladaili.com/gaoni/', 'http://www.xiladaili.com/putong/',
            'http://www.xiladaili.com/https/', 'http://www.xiladaili.com/http/']
    for i in range(2, 50):
        urls.append("http://www.xiladaili.com/putong/{}/".format(i))
        urls.append("http://www.xiladaili.com/http/{}/".format(i))
        urls.append("http://www.xiladaili.com/https/{}/".format(i))
        urls.append("http://www.xiladaili.com/gaoni/{}/".format(i))
    return urls


redis = redis.Redis()


class XilaSpider(scrapy.Spider):
    name = 'xila'
    allowed_domains = []
    start_urls = start_requests()
    # start_urls = ['http://www.xiladaili.com/https/1']

    def parse(self, response):
        html = bs(response.body.decode())
        for tr in html.tbody.findAll('tr'):
            proxy_ip = tr.findAll('td')[0].text
            self.verify_ip(proxy_ip)

    def verify_ip(self, proxy_ip):
        print("开始代理IP检测...")

        proxies = {
            "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
            "https": "http://%(proxy)s/" % {"proxy": proxy_ip},
        }

        try:
            resp = requests.get('https://mockbin.org/request',
                                proxies=proxies, timeout=1)
            if resp.status_code == 200:
                print(resp.json())
                print("代理IP {} 检测成功, 入库中...".format(proxy_ip))
                redis.sadd("PROXY_IPS", proxy_ip)

            return False

        except Exception as err:
            print(err)
            print("代理IP {} 检测已失效, 清理中...".format(proxy_ip))
