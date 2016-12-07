# -*- coding: utf-8 -*-
import random
from scrapy import log
import logging

class ProxyMiddleware(object):
    proxyList = [ \
        '124.88.67.52:843'
        ]

    def process_request(self, request, spider):
        # Set the location of the proxy
        pro_adr = random.choice(self.proxyList)
        log.msg("Current Proxy <%s>" % pro_adr,_level=logging.INFO)
        request.meta['proxy'] = "http://" + pro_adr

