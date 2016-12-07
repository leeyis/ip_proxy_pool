# -*- coding: utf-8 -*-


ITEM_PIPELINES ={
    'main.spiders.pipelines.DuplicatesPipeline': 200,
    'main.spiders.pipelines.IpProxyPoolPipeline': 300,
}

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html, application/xhtml+xml, application/xml',
  'Accept-Language': 'zh-CN,zh;q=0.8'}

DOWNLOADER_MIDDLEWARES = {
    'main.spiders.middlewares.useragent_middlewares.UserAgent': 1,
    'main.spiders.middlewares.proxy_middlewares.ProxyMiddleware': 100,
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware' : None,
}



# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#爬取间隔
DOWNLOAD_DELAY = 1

# 禁用cookie
COOKIES_ENABLED = False