import feedparser
import requests
import json
import re
import os

CURRENT_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

URL = 'https://inciweb.nwcg.gov/feeds/rss/incidents/state/27/'
OUTPUT_FILENAME = os.path.join(CURRENT_PATH, 'incidents.json')


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'asjson'):
            return obj.asjson()
        else:
            return json.JSONEncoder.default(self, obj)


class FireEntry(object):
    LINK_REGEX = re.compile(r'https://inciweb.nwcg.gov/incident/(?P<id>\d+)/')

    def __init__(self,
                 summary_detail=None,
                 links=None,
                 published_parsed=None,
                 title=None,
                 geo_lat=None,
                 summary=None,
                 guidislink=None,
                 title_detail=None,
                 link=None,
                 published=None,
                 geo_long=None,
                 id=None,
                 where=None, *args, **kwargs):
        self.summary_detail = summary_detail
        self.links = links
        self.published_parsed = published_parsed
        self.title = title
        self.geo_lat = geo_lat
        self.summary = summary
        self.guidislink = guidislink
        self.title_detail = title_detail
        self.link = link
        self.published = published
        self.geo_long = geo_long
        self.id = id
        self.where = where

    def asjson(self):
        return self.__dict__

    @property
    def incident_id(self):
        return self.LINK_REGEX.search(self.id).group('id')

    @property
    def cleaned_title(self):
        return self.title.replace('(Wildfire)', '')


class FireEntries(list):
    @classmethod
    def from_rss(cls, rss_entries):
        self = cls()
        for entry in rss_entries:
            self.append(FireEntry(**entry))
        return self

    @classmethod
    def from_file(cls, filename):
        if not os.path.exists(filename):
            return cls()
        return cls.from_rss(json.load(open(filename, 'r')).values())

    def add_by_id(self, fire_entry):
        if fire_entry.incident_id not in self.by_id():
            self.append(fire_entry)

    def by_id(self):
        to_ret = {}
        for entry in self:
            to_ret[entry.incident_id] = entry
        return to_ret

    def asjson(self):
        return self.by_id()


def main():
    data = feedparser.parse(requests.get(URL).text)
    current_entries = FireEntries.from_file(OUTPUT_FILENAME)
    fire_entries = FireEntries.from_rss(data['entries'])
    for entry in fire_entries:
        current_entries.add_by_id(entry)
    json.dump(current_entries.by_id(), open(OUTPUT_FILENAME, 'w'), cls=JSONEncoder)


if __name__ == '__main__':
    main()
