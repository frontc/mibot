# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime, Column, Text
import time

Base = declarative_base()


class Hit(Base):
    __tablename__ = 'hit'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    url = Column(String)
    domain = Column(String)
    crawl_time = Column(DateTime, nullable=False)

    def __init__(self, title, content, url, domain):
        self.title = title
        self.content = content
        self.url = url
        self.domain = domain
        self.crawl_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))


class Log(Base):
    __tablename__ = 'log'
    url = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, url):
        self.url = url
        self.timestamp = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
