# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from itemadapter import is_item, ItemAdapter
from scrapy import signals
import random
import time
import requests
import redis
from .settings import ORDER_ID, REDIS_HOST, REDIS_PORT, REDIS_DB, PROXY_KEY


# useful for handling different item types with a single interface
red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                  db=REDIS_DB, decode_responses=True)


class HunterSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HunterDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # if spider.name != 'jx3':
        #     return None

        print("开始请求伪装...")

        ua = random.choice(spider.settings.get('CUSTOM_USER_AGENT'))
        request.headers['user-agent'] = ua

        proxy_ip = get_proxy_ip()
        print("-------------------", type(proxy_ip), proxy_ip)
        if proxy_ip and spider.name != 'ip3366':
            request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy_ip}

        print("使用User-Agent: {} \n完成请求伪装...".format(ua))

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        print("已获取返回数据...")
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('开启爬虫: %s' % spider.name)


def get_proxy_ip():
    return red.srandmember(PROXY_KEY)
    # proxy_ip = red.srandmember(PROXY_KEY)
    # if proxy_ip and verify_ip(proxy_ip):
    #     return proxy_ip
    # else:
    #     api_url = "http://dps.kdlapi.com/api/getdps/?orderid={}&num=1&pt=1&sep=1".format(
    #         ORDER_ID)
    #     proxy_ip = requests.get(api_url).text
    #     verify_ip(proxy_ip)
    #     return proxy_ip


def verify_ip(proxy):
    print("开始代理IP检测...")

    proxies = {
        "http": "http://%(proxy)s/" % {"proxy": proxy},
        "https": "http://%(proxy)s/" % {"proxy": proxy}
    }
    try:
        resp = requests.get('https://api-wanbaolou.xoyo.com/api/buyer/goods/additional_data',
                            proxies=proxies, timeout=5)
        if resp.status_code == 200:
            print("代理IP {} 检测成功, 入库中...".format(proxy))
            # red.sadd(PROXY_KEY, proxy)
            return True

        # red.srem(PROXY_KEY, proxy)
        return False

    except Exception as err:
        print("代理IP {} 检测已失效, 清理中...".format(proxy))
    #    red.srem(PROXY_KEY, proxy)
        return False
