from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, \
    PrimaryKeyConstraint

from alchemy.models import Base


class Show(Base):
    __tablename__ = "show"

    venue_id = Column(Integer, ForeignKey("venue.id"), nullable=False,
        autoincrement=False),
    show_id = Column(Integer, nullable=False, autoincrement=True)
    date = Column(DateTime)
    acts = Column(String)
    messages = Column(String)
    sold_out = Column(Boolean)

    __table_args__ = (
        PrimaryKeyConstraint('venue_id', 'show_id'),
        {},
    )
