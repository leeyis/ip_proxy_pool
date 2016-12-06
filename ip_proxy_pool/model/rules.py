# -*- coding: utf-8 -*-

from sqlalchemy import Column,String,Integer
from sqlalchemy import Sequence
from . import Base

class Rule(Base):
    __tablename__ = 'rules'

    # 表的结构:
    id = Column(Integer, Sequence('id',start=1,increment=1),primary_key=True)#设定自增长主键
    name = Column(String(100),nullable=False)
    allowed_domains = Column(String(500),nullable=False)
    start_urls = Column(String(500),nullable=False)
    next_page = Column(String(500),nullable=False,default="")
    allow_url = Column(String(500),nullable=False)
    extract_from = Column(String(500),nullable=False,default="")
    loop_xpath = Column(String(500),nullable=False)
    ip_xpath = Column(String(500),nullable=False)
    port_xpath = Column(String(500),nullable=False,default="")
    location1_xpath = Column(String(500),nullable=False)
    location2_xpath = Column(String(500),nullable=False,default="")
    speed_xpath = Column(String(500),nullable=False,default="")
    lifetime_xpath = Column(String(500),nullable=False,default="")
    type_xpath = Column(String(500),nullable=False,default="")
    level_xpath = Column(String(500),nullable=False,default="")
    lastcheck_xpath = Column(String(500),nullable=False,default="")
    enable = Column(Integer,nullable=False)


