from sqlalchemy import Column, Integer, String

from alchemy.models import Base


class Venue(Base):
    __tablename__ = 'venue'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
