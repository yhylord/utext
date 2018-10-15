import scrapy
from utext.helpers import filter_texts, get_page_name


class UTSpider(scrapy.Spider):
    allowed_domains = ['*.utexas.edu']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        texts = response.css(self.selector).extract()
        clean_texts = filter_texts(texts)

        page_name = get_page_name(response.url)
        filename = '{}_{}.txt'.format(self.name, page_name)

        with open(filename, 'w') as f:
            f.write('\n'.join(clean_texts))
        self.log('Write file ' + filename)
