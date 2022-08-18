import pandas as pd
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import and_, asc, desc, or_
from offer_search.model import Offervault_Offer, Affpay_Offer, Odigger_Offer

sqlconn = 'mysql+pymysql://root:1101syw@localhost:3306/youtube_twitter_url?charset=utf8mb4'


def main():
    df = pd.read_csv('./twitter_0818.csv', engine='python')
    df.match_results = None # 我根本不知道为什么！！！！
    engine = create_engine(sqlconn, echo=True, max_overflow=16)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    unique_domains = df['domain'].unique()
    for index, domain in enumerate(unique_domains):
        print("Index_{0}: {1}".format(index, domain))
        condition = '%' + domain + '%'
        results = {}
        rows = session.query(Offervault_Offer).filter(Offervault_Offer.land_page.like(condition)).all()
        if rows:
            for row in rows:
                results[row.url] = row.land_page
        rows = session.query(Affpay_Offer).filter(Affpay_Offer.land_page.like(condition)).all()
        if rows:
            for row in rows:
                results[row.url] = row.land_page
        rows = session.query(Odigger_Offer).filter(Odigger_Offer.land_page.like(condition)).all()
        if rows:
            for row in rows:
                results[row.url] = row.land_page
        if results:
            print(results)
            i_list = df.loc[df['domain'] == domain].index.to_list()
            for i in i_list:
                df.at[i, 'match_results'] = results
    df.to_csv('./result_0818.csv', index=False)
    session.close()


if __name__ == "__main__":
    main()
