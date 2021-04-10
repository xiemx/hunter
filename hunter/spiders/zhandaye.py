import scrapy
from bs4 import BeautifulSoup as bs

import requests
import redis


class ZhandayeSpider(scrapy.Spider):
    name = 'zhandaye'
    allowed_domains = ['zdaye.com']
    start_urls = ['https://www.zdaye.com/dayProxy.html']

    def parse(self, response):
        # print(response.body.decode())
        html = bs(response.body)
        print(html)
        print(html.find_all('a', herf=True))

        # for tr in html.tbody.findAll('tr'):
        #     proxy_ip = '{}:{}'.format(tr.findAll(
        #         'td')[0].text, tr.findAll('td')[1].text)

        #     print(proxy_ip)
        #     #         proxy_ip = ":".join([td.text for td in tr.findAll(
        #     #             'td') if td['data-title'] == 'IP' or td['data-title'] == 'PORT'])

        #     # self.verify_ip(proxy_ip)
