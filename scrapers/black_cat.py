import json
import re
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker

from alchemy import connect
from alchemy.models import Show, Venue
from datetime import datetime
import dateutil.parser as dateparser

from settings import DB, USER, PASSWORD


class BlackCatScraper(object):
    name = "Black Cat"
    url = "http://www.blackcatdc.com/schedule.html"

    def __init__(self):
        self.conn = connect(DB, USER, PASSWORD)
        Session = sessionmaker(bind=self.conn)
        session = Session()
        venue = session.query(Venue).filter_by(name=self.name).first()
        self.venue_id = venue.id
        print("Black Cat venue ID:", self.venue_id)
        self.shows = []

    def scrape(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "lxml")
        main_calendar = soup.select_one("div#main-calendar")
        show_divs = main_calendar.select("div.show")
        for show_div in show_divs:
            show_args = {
                "acts": [],
                "messages": []
            }

            acts = show_div.find_all(class_=re.compile("(headline|support)"))

            for act in acts:
                if act.text == "UPCOMING:":
                    # TODO: handle UPCOMING shows div properly
                    return

                # TODO: try to determine a show "title", like e.g. the headline
                # act or if it's a dance party/other event, split on the
                # "featuring" line, or the line that ends with "presents:", etc.
                if act.text.lower().strip(":") in ["feat", "featuring"]:
                    # Some lines just say "feat" or "featuring", not a real act:
                    continue

                if "SOLD OUT" in act.text:
                    show_args['sold_out'] = True
                else:
                    show_args['acts'].append(act.text)

            messages = show_div.select("p.show-text")
            for message in messages:
                show_args['messages'].append(message.text)

            date_text = show_div.select_one("h2.date").text
            # Throw away the day of the week:
            date_text = date_text.split(None, 1)[1]
            now = datetime.now()
            # TODO: black cat website doesn't have a year associated with its
            # dates, so when the date rolls over to January, we need to
            # understand that it is January of the next year
            date_text += " {}".format(now.year)
            date = datetime.strptime(date_text, "%b %d %Y")
            show_args['date'] = date

            self.add_show(show_args)

    def add_show(self, show_args):
        self.shows.append(show_args)

    def add_show_db(self, show_args):
        # store list-valued arguments to json:
        for key in ['acts', 'messages']:
            show_args[key] = json.dumps(show_args.get(key, []))

        show_args['venue_id'] = self.venue_id

        Session = sessionmaker(bind=self.conn)
        session = Session()

        show = Show(**show_args)
        session.add(show)

        session.commit()


def dump_shows():
    scraper = BlackCatScraper()
    scraper.scrape()
    with open("shows_example.txt", 'w') as f:
        for show_args in scraper.shows:
            show_args['date'] = show_args['date'].isoformat()
            f.write(json.dumps(show_args))
            f.write('\n')


def load_shows_from_file():
    scraper = BlackCatScraper()
    with open("shows_example.txt", 'r') as f:
        for line in f:
            show_args = json.loads(line.strip())
            show_args['date'] = dateparser.parse(show_args['date'])
            scraper.add_show_db(show_args)

if __name__ == "__main__":
    load_shows_from_file()
