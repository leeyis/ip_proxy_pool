#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import socket
import Queue
import datetime
import random
import urllib2
import httplib

import MySQLdb
from lxml import etree as ET
from main.spiders.model.proxy import Proxy
from main.spiders.model.freshProxy import freshProxy
from main.spiders.model import loadSession

SHARE_Q = Queue.Queue()  #构造一个不限制大小的的队列,存放待验证的代理
ACTIVE_Q = Queue.Queue() #构造一个不限制大小的的队列,存放活动的代理
VALID_PROXY = [] #存放有效的代理

_WORKER_THREAD_NUM = 200   #设置线程个数
class MyThread(threading.Thread) :
    def __init__(self, func) :
        super(MyThread, self).__init__()
        self.func = func
    def run(self) :
        self.func()

def checkProxy(proxyIP=None,protocol="http",timeout=5):
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) "
        "AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) "
        "AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; "
        ".NET4.0C; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) "
        "AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; "
        "AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; "
        "Acoo Browser; SLCC1; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; "
        "AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; "
        "Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; "
        "Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727;.NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; "
        ".NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 "
        "(KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ "
        "(KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) "
        "Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) "
        "Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) "
        "Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 "
        "(KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 "
        "(KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "ip.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(user_agent_list)
    }
    urllib2.socket.setdefaulttimeout(timeout)
    if proxyIP:
        proxy_handler = urllib2.ProxyHandler({protocol: "%s://%s" % (protocol, proxyIP)})
    else:
        proxy_handler = urllib2.ProxyHandler({})

    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    req = urllib2.Request("http://ip.cn", headers=headers)
    result = {}


    try:
        starttime = datetime.datetime.now()
        response = urllib2.urlopen(req).read()
        try:
            html = ET.HTML(response)
            if html is not None:
                tmp_rstIP = html.xpath("//div[@id='result']/div[@class='well']/p[1]/code/text()")
                rstIP = tmp_rstIP[0] if len(tmp_rstIP) else ""
                tmp_rstLocation = html.xpath("//div[@id='result']/div[@class='well']/p[2]/code/text()")
                rstLocation = tmp_rstLocation[0] if len(tmp_rstLocation) else ""
                cost = (datetime.datetime.now() - starttime).seconds
            else:
                rstIP = ""

        except ET.XMLSyntaxError,e:
            rstIP=""

        if rstIP:
            result["rstIP"] = rstIP
            result["rstLocation"] = rstLocation
            result["cost"] = cost
            result["status"] = "ok"
            return result
        else:
            result["msg"] = "get ip info failed!"
            result["status"] = "error"
            return result
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            result["status"]="error"
            result["reason"] = e.reason
            result["msg"] = "Failed to reach the server!"
            return result
        elif hasattr(e, "code"):
            result["status"] = "error"
            result[" code"] =  e.code
            result["msg"] = "The server couldn't fulfill the request!"
        else:
            result["msg"] = "unknown error!"
            result["status"] = "error"
            return result
    except urllib2.socket.timeout,e:
        result["status"] = "error"
        result["msg"] = e.message
        return result
    except socket.error,e:
        result["status"] = "error"
        result["msg"] = e.message
    except httplib.BadStatusLine, e:
        result["status"] = "error"
        result["msg"] = e.message

def worker() :
    global SHARE_Q
    while not SHARE_Q.empty():
        item = SHARE_Q.get() #获得任务
        checkActive(item)

def deleteProxy(item):
    session = loadSession()
    session.query(Proxy).filter(Proxy.ip_port == item.ip_port).delete()
    session.commit()

def checkActive(item):
    global ACTIVE_Q
    ip = item.ip_port.split(":")
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _s.settimeout(2)
        _s.connect((ip[0], int(ip[1])))
        _s.close()
        # print "%s is ok!" % ip_port
        ACTIVE_Q.put(item)
    except:
        deleteProxy(item)

def checkValid(item):
    starttime = datetime.datetime.now()
    rst = checkProxy(proxyIP=item.ip_port,protocol="http",timeout=5)
    costtimie = (datetime.datetime.now()-starttime).seconds
    if rst is not None and rst["status"] == "ok":

        proxy = freshProxy(ip_port=item.ip_port,
                           type=item.type,
                           location=rst["rstLocation"].encode("utf-8"),
                           speed=costtimie,
                           source=item.source,
                           rule_id=item.rule_id,
                           lastcheck=datetime.datetime.now()
                           )

        print rst["rstIP"]
        print rst["rstLocation"].encode("utf-8")
        session=loadSession()
        try:
            session.merge(proxy)
            session.commit()
        except MySQLdb.IntegrityError, e:
            print e.message

    else:
        deleteProxy(item)

def main() :
    global SHARE_Q
    global ACTIVE_Q
    threads = []
    session=loadSession()
    proxies = session.query(Proxy).filter(Proxy.type == "HTTP").order_by(Proxy.indate.desc()).limit(20000)

    # 向队列中放入任务
    for proxy in proxies :
        SHARE_Q.put(proxy)

    #控制线程数量
    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker)
        thread.start()
        threads.append(thread)

    for thread in threads :
        thread.join()

    #当队列ACTIVE_Q中的item不为空时循环执行checkValid()
    while not ACTIVE_Q.empty():
        item = ACTIVE_Q.get()
        checkValid(item)

if __name__ == '__main__':
    starttime=datetime.datetime.now()
    main()
    costtimie=(datetime.datetime.now()-starttime).seconds
    print "total cost:%d s" %costtimie