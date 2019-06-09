from selenium import webdriver
from scraper.tokenization import parse_html
import time


def parse_urls(urls):
    driver = webdriver.Chrome('C:\Drivers\chromedriver.exe')
    markup = []

    for url in urls:
        start = time.time()

        driver.get(url);
        html = driver.execute_script("return document.body.outerHTML;")
        parsed = parse_html(html)

        end = time.time()

        markup.append({
            "url": url,
            "data": parsed,
            "time": end - start
        })

    driver.quit()

    return markup
