import scrapy
import json
from ..items import jx3Item
from ..settings import ACCOUNT_API
from datetime import datetime


def start_requests():
    urls = []
    for i in range(1, 1000):
        urls.append(ACCOUNT_API.format(i, 10))

    return urls


class Jx3Spider(scrapy.Spider):

    name = 'jx3'
    allowed_domains = []
    start_urls = start_requests()

    def parse(self, response):

        print("开始抓取用户信息")

        result = json.loads(
            response.body.decode().lstrip('__xfe6(').rstrip(');'))

        for i in result['data']["list"]:

            item = jx3Item()
            item['level'] = i['attrs']['role_level']
            item['equipment_point'] = i['attrs']['role_equipment_point']
            item['experience_point'] = i['attrs']['role_experience_point']
            item['sect'] = i['attrs']['role_sect']
            item['camp'] = i['attrs']['role_camp']
            item['shape'] = i['attrs']['role_shape']
            item['state'] = i['state']
            item['single_unit_size'] = i['single_unit_size']
            item['remain_unit_count'] = i['remain_unit_count']
            item['zone_id'] = i['zone_id']
            item['server_id'] = i['server_id']
            item['seller_role_name'] = i['seller_role_name']
            item['is_followed'] = i['is_followed']
            item['followed_num'] = i['followed_num']
            item['consignment_id'] = i['consignment_id']
            item['is_new'] = i['is_new']
            item['single_unit_price'] = i['single_unit_price']
            item['remaining_time'] = i['remaining_time']
            item['info'] = i['info']
            item['account_type'] = i['account_type']

            item["update_at"] = datetime.utcnow()

            yield item
