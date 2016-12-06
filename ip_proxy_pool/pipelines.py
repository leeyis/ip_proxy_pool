# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.exceptions import DropItem
import redis
from model import loadSession
from model import proxy
from scrapy import log

import logging
Redis = redis.StrictRedis(host='localhost',port=6379,db=0)

# 去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.exists('ip_port:%s' % item['ip_port']) :
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.set('ip_port:%s' % item['ip_port'],1)
            return item


class IpProxyPoolPipeline(object):

    def process_item(self, item, spider):
        if len(item['ip_port']):
            a = proxy.Proxy(
                ip_port=item['ip_port'],
                type=item['type'],
                level=item['level'],
                location=item['location'],
                speed=item['speed'],
                lifetime=item['lifetime'],
                lastcheck=item['lastcheck'],
                rule_id=item['rule_id'],
                source=item['source']
            )
            session = loadSession()
            try:
                session.merge(a)
                session.commit()
            except MySQLdb.IntegrityError, e:
                log.msg("MySQL Error: %s" % str(e), _level=logging.WARNING)
            return item
        else:
            log.msg("ip_port is invalid!",_level=logging.WARNING)

