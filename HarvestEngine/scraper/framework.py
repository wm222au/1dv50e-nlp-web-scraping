import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.tokenization import parse_html
import time

results = []


class WebScraper(scrapy.Spider):
    name = 'Spider'

    def parse(self, response):
        start = time.time()

        extracted_body = response.css('body').extract()
        html = "".join(extracted_body)
        parsed = parse_html(html)

        end = time.time()

        results.append({
            "url": response.request.url,
            "data": parsed,
            "time": end - start
        })


def parse_urls(urls):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(WebScraper, start_urls=urls)
    process.start()

    return results
