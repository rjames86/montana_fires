# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from pelican.readers import BaseReader, METADATA_PROCESSORS
from pelican import signals
from pelican.utils import pelican_open
from incidents import OUTPUT_FILENAME, FireEntries, main as incident_main
from articles import FireArticle, main as article_main

import json
import re


class JSONReader(BaseReader):
    enabled = True
    file_extensions = ['json']

    def __init__(self, settings):
        super(JSONReader, self).__init__(settings)
        self.incidents = FireEntries.from_file(OUTPUT_FILENAME)

    KEYS = [
        'published_parsed',
        'title',
        'geo_lat',
        'summary',
        'link',
        'published',
        'geo_long',
        'id',
    ]
    METADATA_PROCESSOR_KEYS = {
        'published': 'date'
    }

    def read(self, source_path):
        """Parse content and metadata of markdown files"""
        with pelican_open(source_path) as read_text:
            data = FireArticle(**json.loads(read_text))
        content = data.summary

        METADATA_PROCESSORS['title'] = lambda x, y: re.sub(r'(.*)\s\(.* Wildfire\)', '\g<1>', x)

        metadata = {}
        metadata['category'] = self.process_metadata('category', self.incidents.by_id()[data.incident_id].cleaned_title)
        metadata['slug'] = self.process_metadata('slug', data.fire_article_id)
        for key in self.KEYS:
            if hasattr(data, key):
                name = self.METADATA_PROCESSOR_KEYS.get(key, key)
                meta = self.process_metadata(name, getattr(data, key))
                metadata[name] = meta
        return content, metadata


def download_updates():
    incident_main()
    article_main()


def add_reader(readers):
    download_updates()
    for ext in JSONReader.file_extensions:
        readers.reader_classes[ext] = JSONReader


def register():
    signals.readers_init.connect(add_reader)
