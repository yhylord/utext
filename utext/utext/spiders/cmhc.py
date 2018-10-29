# -*- coding: utf-8 -*-
from utext.spiders.base import UTSpider


class CMHCSpider(UTSpider):
    name = 'cmhc'
    allowed_domains = ['cmhc.utexas.edu']
    start_urls = [
        'https://cmhc.utexas.edu/',
        'https://cmhc.utexas.edu/24hourcounseling.html',
        'https://cmhc.utexas.edu/groups.html',
        'https://cmhc.utexas.edu/mindbodylab.html',
        'https://cmhc.utexas.edu/thrive/'
    ]
    selector = 'div.container-fluid ::text'
