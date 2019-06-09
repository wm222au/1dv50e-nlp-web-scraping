import scrapy
from bs4 import BeautifulSoup
from data.urls import LIST

class WebScraper(scrapy.Spider):
    name = 'Spider'
    start_urls = LIST

    def parse(self, response):
        extracted_body = response.xpath('//body//text()').extract()
        print(self.remove_html_markup(extracted_body))

    def remove_html_markup(self, html):
        markup = []
        for token in html:
            markup.append(BeautifulSoup(token, "html.parser").text)

        return markup





