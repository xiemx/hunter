
import redis
import random
from .settings import (REDIS_HOST,
                       REDIS_PORT,
                       REDIS_DB,
                       PROXY_KEY,
                       COOKIE_KEY,
                       CUSTOM_USER_AGENT)

red = redis.Redis(host=REDIS_HOST,
                  port=REDIS_PORT,
                  db=REDIS_DB,
                  decode_responses=True)


def get_user_agent():
    return random.choice(CUSTOM_USER_AGENT)


def get_cookie():
    return red.srandmember(COOKIE_KEY)


def get_proxy_ip():
    return red.srandmember(PROXY_KEY)


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
            return True
        return False

    except Exception as err:
        print("代理IP {} 检测已失效, 清理中...".format(proxy))
        return False
