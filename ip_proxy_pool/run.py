# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from main.spiders.model.rules import Rule
from main.spiders.model import loadSession
from main.spiders.proxy_spider import ProxySpiderSpider

settings = Settings()

# crawl settings

settings.set("ITEM_PIPELINES" , {
    'main.spiders.pipelines.DuplicatesPipeline': 200,
    'main.spiders.pipelines.IpProxyPoolPipeline': 300,
})

settings.set("DEFAULT_REQUEST_HEADERS",{
  'Accept': 'text/html, application/xhtml+xml, application/xml',
  'Accept-Language': 'zh-CN,zh;q=0.8'}
)

settings.set("DOWNLOADER_MIDDLEWARES",{
    'main.spiders.middlewares.useragent_middlewares.UserAgent': 1,
    'main.spiders.middlewares.proxy_middlewares.ProxyMiddleware': 100,
   'scrapy.downloadermiddleware.useragent.UserAgentMiddleware' : None,
}
)

settings.set("DOWNLOAD_DELAY",1)

settings.get("COOKIES_ENABLED",False)

settings.get("ROBOTSTXT_OBEY",True)

process = CrawlerProcess(settings)

session=loadSession()


rules = session.query(Rule).filter(Rule.enable == 1)
for rule in rules:
    print rule.id
    process.crawl(ProxySpiderSpider,rule)
process.start()