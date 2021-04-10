import scrapy
from bs4 import BeautifulSoup as bs

import requests
import redis


redis = redis.Redis()


def start_requests():
    urls = []
    for i in range(1, 10):
        urls.append("http://www.ip3366.net/?stype=1&page={}".format(i))
        urls.append("http://www.ip3366.net/free?stype=2&page={}".format(i))

    return urls


class Ip3366Spider(scrapy.Spider):
    name = 'ip3366'
    allowed_domains = []
    # start_urls = ['http://www.ip3366.net/?stype=1&page=1']
    start_urls = start_requests()

    def parse(self, response):
        # print(response.body.decode())
        html = bs(response.body)

        for tr in html.tbody.findAll('tr'):
            proxy_ip = '{}:{}'.format(tr.findAll(
                'td')[0].text, tr.findAll('td')[1].text)

            print(proxy_ip)
            #         proxy_ip = ":".join([td.text for td in tr.findAll(
            #             'td') if td['data-title'] == 'IP' or td['data-title'] == 'PORT'])

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
