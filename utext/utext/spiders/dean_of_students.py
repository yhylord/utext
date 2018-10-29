# -*- coding: utf-8 -*-
from utext.spiders.base import UTSpider


class DeanOfStudentsSpider(UTSpider):
    name = 'deanofstudents'
    allowed_domains = ['deanofstudents.utexas.edu']
    start_urls = [
        'http://deanofstudents.utexas.edu/conduct/',
        'http://deanofstudents.utexas.edu/emergency/',
        'http://deanofstudents.utexas.edu/emergency/titleix.php',
        'http://deanofstudents.utexas.edu/leadership/',
        'http://deanofstudents.utexas.edu/lss/',
        'http://deanofstudents.utexas.edu/sa/',
        'http://deanofstudents.utexas.edu/sfl/contact.php',
        'http://deanofstudents.utexas.edu/veterans/contact.php'
    ]
    selector = 'div#content ::text'
