import re
import requests
from bs4 import BeautifulSoup
from models import Show
from datetime import datetime

schedule_url = "http://www.blackcatdc.com/schedule.html"


def scrape():
    page = requests.get(schedule_url)
    soup = BeautifulSoup(page.text, "lxml")
    main_calendar = soup.select_one("div#main-calendar")
    show_divs = main_calendar.select("div.show")
    for show_div in show_divs:
        show_builder = Show.builder()

        acts = show_div.find_all(class_=re.compile("(headline|support)"))

        for act in acts:
            if act.text == "UPCOMING:":
                # TODO: handle UPCOMING shows div properly
                return

            # TODO: try to determine a show "title", like e.g. the headline act
            # or if it's a dance party/other event, split on the "featuring"
            # line, or the line that ends with "presents:", etc...
            if act.text.lower.strip(":") in ["feat", "featuring"]:
                # Some lines just say "feat" or "featuring", not a real act...
                continue

            if "SOLD OUT" in act.text:
                show_builder.sold_out()
            else:
                show_builder.add_act(act.text)

        messages = show_div.select("p.show-text")
        for message in messages:
            show_builder.add_message(message.text)

        date_text = show_div.select_one("h2.date").text
        # Throw away the day of the week:
        date_text = date_text.split(None, 1)[1]
        now = datetime.now()
        # TODO: black cat website doesn't have a year associated with its dates,
        # so when the date rolls over to January, we need to understand that it
        # is January of the next year
        date_text += " {}".format(now.year)
        date = datetime.strptime(date_text, "%b %d %Y")
        show_builder.set_date(date)

        print(show_builder.build().dumps())


if __name__ == "__main__":
    scrape()
