# -*- coding: utf-8 -*-
from model import loadSession
from model import proxy
from model.rules import Rule

from model import Base,engine


Base.metadata.create_all(engine)


session = loadSession()
item=Rule()
item.name="ip84"
item.allowed_domains="ip84.com"
item.start_urls="http://ip84.com/gn/1"
item.next_page="//a[@class='next_page']"
item.allow_url="/gn/\d+"
item.loop_xpath="//table[@class='list']/tr[position()>1]"
item.ip_xpath="td[1]/text()"
item.port_xpath="td[2]/text()"
item.location1_xpath="td[3]/a[1]/text()"
item.location2_xpath="td[3]/a[2]/text()"
item.speed_xpath="td[6]/text()"
item.type_xpath="td[5]/text()"
item.level_xpath="td[4]/text()"
item.enable="1"

session.add(item)
session.commit()

