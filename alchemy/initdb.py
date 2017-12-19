import json

from sqlalchemy.orm import sessionmaker

from alchemy import Base, connect
from alchemy.models.venue import Venue
from settings import DB, USER, PASSWORD


def initdb():
    conn = connect(DB, USER, PASSWORD)

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
