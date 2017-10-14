import requests
from bs4 import BeautifulSoup

schedule_url = "http://www.blackcatdc.com/schedule.html"


def scrape():
    page = requests.get(schedule_url)
    soup = BeautifulSoup(page.text, "lxml")
    main_calendar = soup.select_one("div#main-calendar")
    shows = main_calendar.select("div.show")
    for show in shows:
        print(show.prettify())
        show_date = show.select_one("h2.date")
        #print(show_date.text)


if __name__ == "__main__":
    scrape()
