# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import IpProxyPoolItem
from model.spider_running_log import SpiderCrawlLog
from model import loadSession
from datetime import datetime
class ProxySpiderSpider(CrawlSpider):
    name = 'MagicSpider'
    def __init__(self,rule):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allowed_domains.split(',')
        self.start_urls = rule.start_urls.split(',')
        rule_list = []

        # 添加`下一页`的规则
        if len(rule.next_page):
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page), follow=True))

        rule_list.append(Rule(LinkExtractor(
            allow=rule.allow_url.split(','),
            unique=True),
            follow=True,
            callback='parse_item'))

        self.rules = tuple(rule_list)
        super(ProxySpiderSpider, self).__init__()

    def spider_closed(self, spider):
        print "spider is closed!"
        session = loadSession()
        log = session.query(SpiderCrawlLog).filter(SpiderCrawlLog.spiderID == self.rule.id
                                                   and SpiderCrawlLog.endTime is None
                                                   ).first()
        log.endTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.commit()

        pass

    def spider_opened(self, spider):
        print "spider is running!"
        item = SpiderCrawlLog(
                              spiderID=self.rule.id,
                              spiderName=self.rule.name,
                              status="Running...",
                              startTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              endTime=None,
                              pages=0,
                              items=0
                              )
        session = loadSession()
        log = session.query(SpiderCrawlLog).filter(
            SpiderCrawlLog.spiderID == self.rule.id
            and SpiderCrawlLog.endTime is None)

        # 查询当前spider是否有未结束的日志
        if len(log) == 0:
            session.add(item)
            session.commit()
        else:
            pass

    def parse_item(self, response):
        # print 'Hi, this is an item page! %s' % response.url
        # print response.body

        session = loadSession()
        log = session.query(SpiderCrawlLog).filter(SpiderCrawlLog.spiderID == self.rule.id
                                                   and SpiderCrawlLog.status == "Running...").first()
        log.pages = int(log.pages) + 1
        session.commit()



        item=IpProxyPoolItem()

        if len(self.rule.loop_xpath):
            # print 'Find %d items!'% len(response.xpath(self.rule.loop_xpath))
            for proxy in response.xpath(self.rule.loop_xpath):
                if len(self.rule.ip_xpath):
                    tmp_ip = proxy.xpath(self.rule.ip_xpath).extract_first()
                    ip = tmp_ip.strip() if tmp_ip is not None else ""
                else:
                    ip = ""
                if len(self.rule.port_xpath):
                    tmp_port = proxy.xpath(self.rule.port_xpath).extract_first()
                    port = tmp_port.strip() if tmp_port is not None else ""
                else:
                    port = ""
                if len(self.rule.location1_xpath):
                    tmp_location1 = proxy.xpath(self.rule.location1_xpath).extract_first()
                    location1 = tmp_location1.strip() if tmp_location1 is not None else ""
                else:
                    location1 = ""
                if len(self.rule.location2_xpath):
                    tmp_location2 = proxy.xpath(self.rule.location2_xpath).extract_first()
                    location2 = tmp_location2.strip() if tmp_location2 is not None else ""
                else:
                    location2 = ""
                if len(self.rule.lifetime_xpath):
                    tmp_lifetime = proxy.xpath(self.rule.lifetime_xpath).extract_first()
                    lifetime = tmp_lifetime.strip() if tmp_lifetime is not None else ""
                else:
                    lifetime = ""
                if len(self.rule.lastcheck_xpath):
                    tmp_lastcheck = proxy.xpath(self.rule.lastcheck_xpath).extract_first()
                    lastcheck = tmp_lastcheck.strip() if tmp_lastcheck is not None else ""
                else:
                    lastcheck = ""
                if len(self.rule.level_xpath):
                    tmp_level = proxy.xpath(self.rule.level_xpath).extract_first()
                    level = tmp_level.strip() if tmp_level is not None else ""
                else:
                    level = ""
                if len(self.rule.type_xpath):
                    tmp_type = proxy.xpath(self.rule.type_xpath).extract_first()
                    type = tmp_type.strip() if tmp_type is not None else ""
                else:
                    type = ""
                if len(self.rule.speed_xpath):
                    tmp_speed = proxy.xpath(self.rule.speed_xpath).extract_first()
                    speed = tmp_speed.strip() if tmp_speed is not None else ""
                else:
                    speed = ""

                item['ip_port']=(":".join([ip,port])) if len(port) else ip
                item['type']=type
                item['level']=level
                item['location']=(" ".join([location1,location2])) if location2 is not None and len(location2) else location1
                item['speed']=speed
                item['lifetime']=lifetime
                item['lastcheck']=lastcheck
                item['rule_id']=self.rule.id
                item['source']=response.url

                yield item