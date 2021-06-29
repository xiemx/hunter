import os
import requests
import redis

red = redis.Redis(decode_responses=True)


def verify_ip(proxy):
    print("开始代理IP检测...")

    proxies = {
        "http": "http://%(proxy)s/" % {"proxy": proxy},
        "https": "http://%(proxy)s/" % {"proxy": proxy},
    }
    try:
        resp = requests.get('http://api-wanbaolou.xoyo.com/api/buyer/goods/additional_data',
                            proxies=proxies, timeout=5)
        if resp.status_code == 200 and  resp.json()['code'] != -13:
            print("代理IP {} 检测成功...".format(proxy))
            return True
        else:
            print(resp.json())
            print("代理IP {} 检测失效...".format(proxy))
            return False

    except Exception as err:
        print(err)
        print("代理IP {} 检测失效...".format(proxy))
        return False


if __name__ == "__main__":
    for ip in red.sscan_iter("PROXY_IPS"):
        count = 0
        while True:
           if verify_ip(ip):
               break

           count = count + 1
           if count > 5:
               print("代理IP {}, 清理中...".format(ip))
               red.srem("PROXY_IPS", ip)
               break

