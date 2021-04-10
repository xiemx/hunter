# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HunterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class jx3Item(scrapy.Item):

    _id = scrapy.Field()

    level = scrapy.Field()  # 等级
    equipment_point = scrapy.Field()  # 装备分
    experience_point = scrapy.Field()  # 江湖资历
    sect = scrapy.Field()  # 职业
    camp = scrapy.Field()  # 阵营
    shape = scrapy.Field()  # 提醒
    state = scrapy.Field()  # 状态
    single_unit_size = scrapy.Field()  # 数量
    remain_unit_count = scrapy.Field()  # 数量
    zone_id = scrapy.Field()  # 区服务器
    server_id = scrapy.Field()
    seller_role_name = scrapy.Field()  # 卖家名
    is_followed = scrapy.Field()  # 是否关注
    followed_num = scrapy.Field()  # 关注数量
    consignment_id = scrapy.Field()  # 订单ID
    is_new = scrapy.Field()
    single_unit_price = scrapy.Field()  # 价格，人民币（分）
    remaining_time = scrapy.Field()  # 当前状态剩余时间
    info = scrapy.Field()  # info "电信五区-斗转星移-不***"
    account_type = scrapy.Field()  # 账号类型
    # "role_base_info",  # 基础信息
    # "role_equipment_info",  # 装备

    # role_appearance_info  外观
    back = scrapy.Field()  # 背部挂件
    backCloak = scrapy.Field()  # 披风
    bag = scrapy.Field()  # 佩囊
    exterior = scrapy.Field()  # 拓印外观
    face = scrapy.Field()  # 面挂
    faceCount = scrapy.Field()  # 面挂数量
    hair = scrapy.Field()  # 发型
    horse = scrapy.Field()  # 坐骑
    lShoudler = scrapy.Field()  # 左肩饰品
    miniAvatar = scrapy.Field()  # 小头像
    hangPet = scrapy.Field()  # 挂物
    rShoudler = scrapy.Field()  # 右肩饰品
    shopExterior = scrapy.Field()  # 商场外观
    waist = scrapy.Field()  # 腰部挂件
    weapon = scrapy.Field()  # 武器拓印

    # role_adventure_info 奇遇
    adventure = scrapy.Field()

    # role_pet_info 宠物
    pet = scrapy.Field()
    petSummary = scrapy.Field()

    # "role_homeland_info",  # 家园
    homelandLevel = scrapy.Field()

    # "role_other_info"  # 其他
    # spar110 = scrapy.Field()  # 小铁

    update_at = scrapy.Field()  # 数据更新时间
