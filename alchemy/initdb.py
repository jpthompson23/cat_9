import json

import sqlalchemy
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DB, USER, PASSWORD

Base = declarative_base()


def connect(user, password, db, host='localhost', port=5432):
    """
    Returns a connection
    """
    # We connect with the help of the PostgreSQL URL
    # postgresql://<user>:<password>@<host>:<port>/<db>
    url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    conn = sqlalchemy.create_engine(url, client_encoding='utf8')

    return conn


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)


def initdb():
    conn = connect(USER, PASSWORD, DB)

    Session = sessionmaker(bind=conn)
    session = Session()

    Base.metadata.drop_all(conn)
    Base.metadata.create_all(conn)

    with open("venues.txt") as venues_file:
        for line in venues_file:
            venue_json = json.loads(line)
            venue = Venue(**venue_json)
            session.add(venue)
    session.commit()


if __name__ == "__main__":
    initdb()
