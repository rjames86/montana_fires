# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as Soup
import requests
import re


class FireAnnoucement(object):
    def __init__(self, title, text, incident_url, article_url):
        self.title = title
        self.text = text
        self.incident_url = incident_url
        self.article_url = article_url

    @classmethod
    def from_soup_object(cls, soup_object):
        if soup_object.text.endswith('...'):

        else:
            return cls(
                title=soup_object.find('a').text,
                text=soup_object.text,
                incident_url=soup_object.find('a', href=re.compile(r"/incident/\d+/")),
                article_url=soup_object.find('a', href=re.compile(r"/incident/article/\d+/\d+/"))
            )

class FireAnnouncements(object):
    BASE_URL = 'https://inciweb.nwcg.gov'

    def __init__(self):
        self.current_url = '/state/announcements/27/'
        self.soup = self._get_soup()

    @property
    def nav_list(self):
        return self.soup.find('div', {'class': 'tab_nav'})

    @property
    def current_page(self):
        return self.nav_list.find('strong')

    def update_url(self, url):
        self.current_url = url
        self.soup = self._get_soup()

    def get_annoucement_items(self):
        announcement_list = self.soup.find('ul', id='news_list')
        return announcement_list.findAll('li')

    def get_next_url(self):
        current_page_number = int(self.current_page.text)
        return self.nav_list.find('a', text=str(current_page_number + 1))

    def has_more(self):
        return self.nav_list.find('a', text=re.compile("next.*")) is not None

    def _get_soup(self):
        return Soup(requests.get(self.BASE_URL + self.current_url).text, "html.parser")
