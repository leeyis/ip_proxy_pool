# -*- coding: utf-8 -*-
import scrapy


class IpProxyPoolItem(scrapy.Item):

    ip_port = scrapy.Field()
    type = scrapy.Field()
    level = scrapy.Field()
    location = scrapy.Field()
    speed = scrapy.Field()
    lifetime = scrapy.Field()
    lastcheck = scrapy.Field()
    rule_id = scrapy.Field()
    source = scrapy.Field()