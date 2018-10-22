import scrapy
from utext.helpers import filter_texts, get_page_name


class UTSpider(scrapy.Spider):
    allowed_domains = ['*.utexas.edu']

    def parse(self, response):
        try:
            texts = response.css(self.selector).extract()
        except scrapy.exceptions.NotSupported:
            # if the response body is not text-based (e.g. file)
            return
        clean_texts = filter_texts(texts)

        page_name = get_page_name(response.url)
        if page_name:
            filename = '{}_{}.txt'.format(self.name, page_name)
        else:
            filename = '{}.txt'.format(self.name)

        with open(filename, 'w') as f:
            f.write('\n'.join(clean_texts))
        self.log('Write file ' + filename)

        for href in response.css('a::attr(href)'):
            yield response.follow(href, callback=self.parse)
