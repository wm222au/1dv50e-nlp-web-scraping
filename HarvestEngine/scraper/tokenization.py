from bs4 import BeautifulSoup
import re


def parse_html(html):
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(["script", "style", 'aside']):
        script.extract()

    return filter_text(soup.get_text(separator=u' '))


def filter_text(text):
    return " ".join(re.split(r'[\n\t]+', text))
