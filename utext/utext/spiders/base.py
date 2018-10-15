import scrapy
from utext.helpers import filter_texts, get_page_name


class UTSpider(scrapy.Spider):
    allowed_domains = ['*.utexas.edu']

    def parse(self, response):
        texts = response.css(self.selector).extract()
        clean_texts = filter_texts(texts)

        page_name = get_page_name(response.url)
        if page_name:
            filename = '{}_{}.txt'.format(self.name, page_name)
        else:
            filename = '{}.txt'.format(self.name)

        with open(filename, 'w') as f:
            f.write('\n'.join(clean_texts))
        self.log('Write file ' + filename)
