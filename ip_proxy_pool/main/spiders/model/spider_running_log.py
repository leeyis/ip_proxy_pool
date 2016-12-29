# -*- coding: utf-8 -*-
from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy import Sequence
from . import Base

class SpiderCrawlLog(Base):
    __tablename__ = 'SpiderCrawlLog'
    # 表的结构:
    id = Column(Integer, Sequence('id', start=1, increment=1), primary_key=True)  # 设定自增长主键
    spiderID = Column(Integer,nullable=False)
    spiderName = Column(String(50),nullable=False)
    status = Column(String(20),nullable=False)
    startTime = Column(DateTime,nullable=True)
    endTime = Column(DateTime,nullable=True)
    pages = Column(Integer,nullable=False,default=0)
    items = Column(Integer,nullable=False,default=0)

    def __init__(self,spiderID,spiderName,status,startTime,endTime,pages,items):
        self.spiderID = spiderID
        self.spiderName = spiderName
        self.status = status
        self.startTime = startTime
        self.endTime = endTime
        self.pages = pages
        self.items = items
