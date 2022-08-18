from sqlalchemy import Column, String, create_engine, Integer, SmallInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql

Base = declarative_base()


# 定义对象
class Affpay_Offer(Base):
    # 表名
    __tablename__ = 'affpay_offer'

    id = Column(mysql.BIGINT, primary_key=True)
    url = Column(String(1024))
    title = Column(String(600))
    payout = Column(String(32))
    status = Column(String(24))
    offer_create_time = Column(String(32))
    offer_update_time = Column(String(32))
    category = Column(String(256))
    geo = Column(String(2048))
    network = Column(String(32))
    description = Column(String(10000))
    land_page = Column(String(1024))
    create_time = Column(mysql.BIGINT)


class Offervault_Offer(Base):
    # 表名
    __tablename__ = 'offervault_offer'

    id = Column(mysql.BIGINT, primary_key=True)
    url = Column(String(1024))
    title = Column(String(600))
    payout = Column(String(32))
    offer_create_time = Column(String(32))
    offer_update_time = Column(String(32))
    category = Column(String(256))
    geo = Column(String(2048))
    network = Column(String(256))
    description = Column(String(10000))
    land_page = Column(String(1024))
    create_time = Column(mysql.BIGINT)


class Odigger_Offer(Base):
    # 表名
    __tablename__ = 'odigger_offer'

    id = Column(mysql.BIGINT, primary_key=True)
    url = Column(String(1024))
    title = Column(String(600))
    payout = Column(String(32))
    offer_create_time = Column(String(32))
    offer_update_time = Column(String(32))
    category = Column(String(256))
    geo = Column(String(2048))
    network = Column(String(256))
    description = Column(String(10000))
    land_page = Column(String(1024))
    status = Column(String(24))
    create_time = Column(mysql.BIGINT)
