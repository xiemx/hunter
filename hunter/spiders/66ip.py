import scrapy


import requests
import redis


redis = redis.Redis()


class A66ipSpider(scrapy.Spider):
    name = '66ip'
    allowed_domains = []
    start_urls = ['http://www.66ip.cn/pt.html']

    def parse(self, response):
        resp = requests.get(
            'http://www.66ip.cn/?sxb=&tqsl=10&ports%5B%5D2=&ktip=&sxa=&radio=radio&submit=%CC%E1++%C8%A1')
        print(resp.content.decode())

