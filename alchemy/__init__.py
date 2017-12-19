import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def connect(db, user, password, host='localhost', port=5432):
    """
    Returns a connection
    """
    # We connect with the help of the PostgreSQL URL
    # postgresql://<user>:<password>@<host>:<port>/<db>
    url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    conn = sqlalchemy.create_engine(url, client_encoding='utf8')

    return conn
