import pandas as pd
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import and_, asc, desc, or_


def main():
    landing_page = pd.read_csv('./landing')


if __name__ == "__main__":
    main()