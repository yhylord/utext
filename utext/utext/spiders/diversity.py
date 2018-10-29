# -*- coding: utf-8 -*-
from utext.spiders.base import UTSpider


class DiversitySpider(UTSpider):
    name = 'diversity'
    allowed_domains = ['diversity.utexas.edu']
    start_urls = [
        # TODO fix getting all contents on /disability/
        'http://diversity.utexas.edu/disability/',
        'http://diversity.utexas.edu/genderandsexuality/',
        'http://diversity.utexas.edu/multiculturalengagement/'
    ]
    selector = 'main.content ::text'
