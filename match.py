import pandas as pd
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import and_, asc, desc, or_
from offer_search.model import Offervault_Offer, Affpay_Offer, Odigger_Offer

sqlconn = 'mysql+pymysql://root:1101syw@localhost:3306/test?charset=utf8mb4'


def main():
    engine = create_engine(sqlconn, echo=True, max_overflow=16)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    with open('./query.txt', 'r') as f:
        query_list = f.readlines()
    for query in query_list:
        query = query.strip('\n')
        q=query
        query = '.'.join(query.split('.')[-2:])
        condition = '%' + query + '%'
        rows = session.query(Offervault_Offer).filter(Offervault_Offer.land_page.like(condition)).all()
        if rows:
            for row in rows:
                if q in row.land_page.split('/')[2]:
                    with open('./results_db.txt', 'a') as f:
                        f.write("{0}\t{1}\t{2}\n".format(q, row.url, row.land_page))
        rows = session.query(Affpay_Offer).filter(Affpay_Offer.land_page.like(condition)).all()
        if rows:
            for row in rows:
                if q in row.land_page.split('/')[2]:
                    with open('./results_db.txt', 'a') as f:
                        f.write("{0}\t{1}\t{2}\n".format(q, row.url, row.land_page))
        rows = session.query(Odigger_Offer).filter(Odigger_Offer.land_page.like(condition)).all()
        if rows:
            for row in rows:
                if q in row.land_page.split('/')[2]:
                    with open('./results_db.txt', 'a') as f:
                        f.write("{0}\t{1}\t{2}\n".format(q, row.url, row.land_page))

    session.close()


if __name__ == "__main__":
    main()
