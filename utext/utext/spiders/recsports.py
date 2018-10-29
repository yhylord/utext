# -*- coding: utf-8 -*-
from utext.spiders.base import UTSpider


class RecSportsSpider(UTSpider):
    name = 'recsports'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5
    }
    allowed_domains = ['www.utrecsports.org']
    start_urls = [
        'https://utrecsports.org/',
        'https://utrecsports.org/fitness-and-wellness',
        'https://utrecsports.org/fitness-and-wellness/texercise',
        'https://utrecsports.org/intramurals',
        'https://utrecsports.org/sport-clubs'
    ]
    selector = '.nine.columns ::text'
