# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import requests
import json
import redis
import time
from datetime import datetime
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .middlewares import get_proxy_ip


from .settings import MONGO_COLLECTION, MONGO_DB, MONGO_URL, REDIS_HOST, REDIS_DB, REDIS_PORT, COOKIE_KEY, DELAY, DOWNLOAD_TIMEOUT

info_list = []


class HunterPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.mongo = self.db[MONGO_COLLECTION]
        self.red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def get_cookie(self):
        return self.red.srandmember(COOKIE_KEY)

    def item_isExist(self, item):
        count = self.mongo.find(
            {"consignment_id": item['consignment_id'], "info": item["info"]}).count()
        return count

    def process_item(self, item, spider):
        global info_list
        additional_keys = [
            {"key": "role_base_info", "enabled": spider.settings.get(
                'BASE'), "func": self.base_info},  # 基础信息
            {"key": "role_equipment_info", "enabled":  spider.settings.get('EQUIPMENT'),
                "func": self.equipment_info},  # 装备
            {"key": "role_appearance_info", "enabled":  spider.settings.get('APPEARANCE'),
                "func": self.appearance_info},  # 外观
            {"key": "role_adventure_info", "enabled":  spider.settings.get('ADVENTURE'),
                "func": self.adventure_info},  # 奇遇
            {"key": "role_pet_info", "enabled":  spider.settings.get(
                'PET'), "func": self.pet_info},  # 宠物
            {"key": "role_homeland_info", "enabled":  spider.settings.get('HOMELAND'),
                "func": self.homeland_info},  # 家园
            {"key": "role_other_info", "enabled":  spider.settings.get(
                'OTHER'), "func": self.other_info}  # 其他
        ]

        for additional_key in additional_keys:
            retry = 0
            while True:
                try:
                    if not additional_key['enabled']:
                        break
                    time.sleep(DELAY)

                    if spider.settings.get("PROXY_ENABLED") or self.red.exists("PROXY_ENABLED"):

                        proxy_ip = get_proxy_ip()
                        proxies = {
                            "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
                            "https": "http://%(proxy)s/" % {"proxy": proxy_ip}
                        }
                        print('使用代理IP {} 伪装请求...'.format(proxy_ip))
                        headers = spider.settings.get(
                            'DEFAULT_REQUEST_HEADERS')
                        headers['cookie'] = self.get_cookie()
                        response = requests.get(spider.settings.get("DETAIL_API").format(
                            item['consignment_id'], additional_key["key"]), headers=headers, proxies=proxies, timeout=DOWNLOAD_TIMEOUT)
                    else:
                        headers = spider.settings.get(
                            'DEFAULT_REQUEST_HEADERS')
                        headers['cookie'] = self.get_cookie()
                        response = requests.get(spider.settings.get("DETAIL_API").format(
                            item['consignment_id'], additional_key["key"]), headers=headers, timeout=DOWNLOAD_TIMEOUT)
                    result = json.loads(
                        response.content.decode().lstrip('__xfe48(').rstrip(');'))
                    print(result.get("msg"))
                    item = additional_key["func"](result, item)
                    break
                except Exception as err:
                    retry = retry + 1
                    if retry > 3:
                        break
                    print("获取 {} {} 信息失败..., 开始第{}次重试...".format(
                        item["info"], additional_key['key'], retry))

        print(item)

        if not self.item_isExist(item):
            info_list.append(item)
            if len(info_list) > 0:
                response = self.mongo.insert_many(info_list)
                if response:
                    print("数据入库成功!")
                    info_list = []
                else:
                    print("数据入库失败!")
        else:
            response = self.mongo.update_one(
                {"consignment_id": item['consignment_id'], "info": item["info"]}, {"$set": item})
            if response:
                print("用户信息更新成功!")
            else:
                print("用户信息更新失败")

    def base_info(self, result, item):
        print("获取用户基础信息...")
        item["update_at"] = datetime.now()
        return item

    def equipment_info(self, item):
        print("获取用户装备信息...")
        item["update_at"] = datetime.now()

        return item

    def pet_info(self, result, item):
        print("获取用户宠物信息...")

        item["pet"] = [i['name']
                       for i in result['data']['additional_data']['pet']]
        item["petSummary"] = result['data']['additional_data']['petSummary']['adventureCount']
        item["update_at"] = datetime.now()
        return item

    def homeland_info(self, result, item):
        print("获取用户家园信息...")
        item["update_at"] = datetime.now()
        item["homelandLevel"] = result['data']['additional_data']['homeland']['level']
        return item

    def adventure_info(self, result, item):
        print("获取用户奇遇信息...")
        item["update_at"] = datetime.now()
        item['adventure'] = [i['name']
                             for i in result['data']['additional_data']['adventure']]
        return item

    def other_info(self, result, item):
        print("获取用户其它信息...")
        item["update_at"] = datetime.now()
        return item

    def appearance_info(self, result, item):
        print('获取用户外观信息...')
        item["update_at"] = datetime.now()

        item["back"] = [i['name']
                        for i in result['data']['additional_data']['appearance']['back']]
        item["backCloak"] = [i['name']
                             for i in result['data']['additional_data']['appearance']['backCloak']]
        item["bag"] = [i['name']
                       for i in result['data']['additional_data']['appearance']['bag']]
        item["exterior"] = ['{}-{}'.format(i['name'], i['type'])
                            for i in result['data']['additional_data']['appearance']['exterior']]
        item["face"] = [i['name']
                        for i in result['data']['additional_data']['appearance']['face']]
        item["faceCount"] = result['data']['additional_data']['appearance']['faceCount']
        item["hair"] = [i['name']
                        for i in result['data']['additional_data']['appearance']['hair']]
        item["horse"] = [i['name']
                         for i in result['data']['additional_data']['appearance']['horse']]
        item["lShoudler"] = [i['name']
                             for i in result['data']['additional_data']['appearance']['lShoudler']]
        item["miniAvatar"] = [i['headUrl']
                              for i in result['data']['additional_data']['appearance']['miniAvatar']]
        item["hangPet"] = [i['name']
                           for i in result['data']['additional_data']['appearance']['pet']]
        item["rShoudler"] = [i['name']
                             for i in result['data']['additional_data']['appearance']['rShoudler']]
        item["shopExterior"] = ['{}-{}'.format(i['name'], i['type'])
                                for i in result['data']['additional_data']['appearance']['shopExterior']]
        item["waist"] = [i['name']
                         for i in result['data']['additional_data']['appearance']['waist']]
        item["weapon"] = [i['name']
                          for i in result['data']['additional_data']['appearance']['weapon']]
        return item
