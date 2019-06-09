import requests
from scraper.tokenization import parse_html
import time


def parse_urls(urls):
    markup = []

    for url in urls:
        start = time.time()

        res = requests.get(url)
        html = res.text
        parsed = parse_html(html)

        end = time.time()

        markup.append({
            "url": url,
            "data": parsed,
            "time": end - start
        })

    return markup




