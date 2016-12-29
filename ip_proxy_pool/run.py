# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from main.spiders import config
from main.spiders.model.rules import Rule
from main.spiders.model import loadSession
from main.spiders.proxy_spider import ProxySpiderSpider

settings = Settings()


settings.set("ITEM_PIPELINES" ,config.ITEM_PIPELINES)

settings.set("DEFAULT_REQUEST_HEADERS",config.DEFAULT_REQUEST_HEADERS)

settings.set("DOWNLOADER_MIDDLEWARES",config.DOWNLOADER_MIDDLEWARES)

settings.set("DOWNLOAD_DELAY",config.DOWNLOAD_DELAY)

settings.set("COOKIES_ENABLED",config.COOKIES_ENABLED)

settings.set("ROBOTSTXT_OBEY",config.ROBOTSTXT_OBEY)

process = CrawlerProcess(settings)

session=loadSession()


rules = session.query(Rule).filter(Rule.enable == 1)
for rule in rules:
    print rule.id
    process.crawl(ProxySpiderSpider,rule)
process.start()