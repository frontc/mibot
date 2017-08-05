# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:odsods@localhost:3306/spider?charset=utf8')
DBSession = sessionmaker(bind=engine)