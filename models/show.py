import json
from datetime import datetime


class ShowBuilder(object):
    def __init__(self):
        self.show = Show()

    def set_date(self, date):
        self.show.date = date
        return self

    def add_act(self, act):
        self.show.acts.append(act)
        return self

    def add_message(self, message):
        self.show.messages.append(message)
        return self

    def sold_out(self):
        self.show.sold_out = True
        return self

    def build(self):
        return self.show


class Show(object):
    def __init__(self):
        self.date = None
        self.acts = []
        self.messages = []
        self.sold_out = False

    @staticmethod
    def builder():
        return ShowBuilder()

    def dumps(self):
        return json.dumps({
            "date": datetime.strftime(self.date, "%Y-%m-%d"),
            "acts": self.acts,
            "messages": self.messages,
            "sold_out": self.sold_out
        }, indent=2)


