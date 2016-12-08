# -*- coding: utf-8 -*-
from sqlalchemy import Column,String,Integer,DateTime

from . import Base
import datetime
class freshProxy(Base):
    __tablename__ = 'fresh_proxies'

    ip_port= Column(String(30),primary_key=True,nullable=False)
    type= Column(String(20),nullable=True,default="")
    level= Column(String(20),nullable=True,default="")
    location= Column(String(100),nullable=True,default="")
    speed= Column(String(20),nullable=True,default="")
    lifetime = Column(String(20),nullable=True,default="")
    lastcheck = Column(String(20),nullable=True,default="")
    source = Column(String(500), nullable=False)
    rule_id = Column(Integer,nullable=False)
    indate = Column(DateTime,nullable=False)

    def __init__(self,ip_port,source="",type="",level="",location="",speed="",lifetime="",lastcheck="",rule_id=""):
        self.ip_port=ip_port
        self.type=type
        self.level=level
        self.location=location
        self.speed=speed
        self.source=source
        self.lifetime=lifetime
        self.lastcheck=lastcheck
        self.rule_id=rule_id
        self.indate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")