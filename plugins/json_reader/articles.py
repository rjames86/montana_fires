import feedparser
import requests
import json
import re
import os
from collections import defaultdict
from bs4 import BeautifulSoup as Soup

URL = 'https://inciweb.nwcg.gov/feeds/rss/articles/state/27/'
OUTPUT_DIR = '/Users/rjames/Dropbox/blogs/montana_fires/content'
OUTPUT_FILENAME = 'articles.json'


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'asjson'):
            return obj.asjson()
        else:
            return json.JSONEncoder.default(self, obj)


class FireArticle(object):
    LINK_REGEX = re.compile(r'https://inciweb.nwcg.gov/incident/article/(?P<id>\d+)/(?P<article_id>\d+)/')

    def __init__(self,
                 summary_detail,
                 published_parsed,
                 links,
                 title,
                 summary,
                 guidislink,
                 title_detail,
                 link,
                 published,
                 id,
                 content=None,
                 *args, **kwargs):
        self.summary_detail = summary_detail
        self.published_parsed = published_parsed
        self.links = links
        self.title = title
        self.summary = summary
        self.guidislink = guidislink
        self.title_detail = title_detail
        self.link = link
        self.published = published
        self.id = id
        self._content = content

    def asjson(self):
        return dict(
            summary_detail=self.summary_detail,
            published_parsed=self.published_parsed,
            links=self.links,
            title=self.title,
            summary=self.summary,
            guidislink=self.guidislink,
            title_detail=self.title_detail,
            link=self.link,
            published=self.published,
            id=self.id,
            incident_id=self.incident_id,
            article_id=self.article_id,
            content=self.content
        )

    @property
    def incident_id(self):
        return self.LINK_REGEX.search(self.id).group('id')

    @property
    def article_id(self):
        return self.LINK_REGEX.search(self.id).group('article_id')

    @property
    def fire_article_id(self):
        return "{item.incident_id}_{item.article_id}".format(item=self)

    @property
    def content(self):
        if self._content is None:
            if self.summary.endswith('...'):
                soup = Soup(requests.get(self.id).text, "html.parser")
                self._content = unicode(soup.find('div', id='content'))
            else:
                self._content = self.summary
        return self._content


class FireArticles(list):
    @classmethod
    def from_rss(cls, rss_entries):
        self = cls()
        for entry in rss_entries:
            article = FireArticle(**entry)
            if not os.path.exists(os.path.join(OUTPUT_DIR, '%s.json' % article.fire_article_id)):
                self.append(article)
        return self

    @classmethod
    def from_file(cls, filename):
        if not os.path.exists(filename):
            return cls()
        return cls.from_rss(json.load(open(filename, 'r')).values())

    def add_by_id(self, fire_entry):
        if fire_entry.fire_article_id not in self.by_id():
            self.append(fire_entry)

    def by_id(self):
        to_ret = {}
        for entry in self:
            to_ret[entry.fire_article_id] = entry
        return to_ret

    def by_incident(self):
        to_ret = defaultdict(list)
        for entry in self:
            to_ret[entry.incident_id].append(entry)
        return to_ret

    def asjson(self):
        return self.by_id()


def main():
    data = feedparser.parse(requests.get(URL).text)
    fire_entries = FireArticles.from_rss(data['entries'])

    for entry in fire_entries:
        with open(os.path.join(OUTPUT_DIR, '%s.json' % entry.fire_article_id), 'w') as f:
            json.dump(entry, f, sort_keys=True, indent=4, separators=(',', ': '), cls=JSONEncoder)


if __name__ == '__main__':
    main()
