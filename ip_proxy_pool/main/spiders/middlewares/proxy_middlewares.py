# -*- coding: utf-8 -*-
import random
from scrapy import log
import logging
from ..model import loadSession
from ..model.freshProxy import freshProxy
class ProxyMiddleware(object):
    session=loadSession()
    proxies = session.query(freshProxy).order_by(freshProxy.indate.desc()).all()
    proxyList = []
    for proxy in proxies:
        if proxy.ip_port not in proxyList:
            proxyList.append(proxy.ip_port)
        else:
            pass


    def process_request(self, request, spider):
        # Set the location of the proxy
        pro_adr = random.choice(self.proxyList)
        log.msg("Current Proxy <%s>" % pro_adr,_level=logging.INFO)
        request.meta['proxy'] = "http://" + pro_adr

