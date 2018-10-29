# -*- coding: utf-8 -*-
from utext.spiders.base import UTSpider


class UHSSpider(UTSpider):
    name = 'uhs'
    allowed_domains = ['healthyhorns.utexas.edu']
    start_urls = [
        'https://healthyhorns.utexas.edu/allergyshots.html',
        'https://healthyhorns.utexas.edu/dietitian.html',
        'https://healthyhorns.utexas.edu/gmc.html',
        'https://healthyhorns.utexas.edu/healthpromotion.html',
        'https://healthyhorns.utexas.edu/hs_uhssexualassaultforensicexams.html',
        'https://healthyhorns.utexas.edu/hs_uhsstitesting.html',
        'https://healthyhorns.utexas.edu/physicaltherapy.html',
        'https://healthyhorns.utexas.edu/sportsmedicine.html',
        'https://healthyhorns.utexas.edu/travel/',
        'https://healthyhorns.utexas.edu/womenshealth.html'
    ]
    selector = 'div.container div.container-fluid ::text'
