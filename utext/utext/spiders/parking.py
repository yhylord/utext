# -*- coding: utf-8 -*-
from utext.spiders.base import UTSpider


class ParkingSpider(UTSpider):
    name = 'parking'
    allowed_domains = ['parking.utexas.edu']
    start_urls = [
        'https://parking.utexas.edu/bike',
        'https://parking.utexas.edu/services/longhorn-auto-assistance-program',
        'https://parking.utexas.edu/sure',
        'https://parking.utexas.edu/transportation/shuttles'
    ]
    selector = 'section.main-content ::text'
