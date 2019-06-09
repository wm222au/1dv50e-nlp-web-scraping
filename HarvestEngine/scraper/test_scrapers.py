from scraper.automation import parse_urls as auto_parse
from scraper.framework import parse_urls as frame_parse
from scraper.network_request import parse_urls as nr_parse
from scraper.en_urls import LIST

import time
from operator import itemgetter


def sort_by_url(list):
    return sorted(list, key=itemgetter('url'), reverse=True)


# Testing automation parsing
start = time.time()
auto = auto_parse(LIST)
end = time.time()
print("Automation", end - start)

# Testing framework parsing
start = time.time()
frame = frame_parse(LIST)
end = time.time()
print("Framework", end - start)

# Testing network request parsing
start = time.time()
nr = nr_parse(LIST)
end = time.time()
print("Network request", end - start)

auto_s = sort_by_url(auto)
frame_s = sort_by_url(frame)
nr_s = sort_by_url(nr)


for i in range(len(auto)):
    a = auto_s[i]
    f = frame_s[i]
    n = nr_s[i]

    print("Iteration: ", i)
    print("Same url: ", a['url'] == f['url'] and a['url'] == n['url'] and n['url'] == f['url'])
    print(len(a['data']), a['time'])
    print(len(f['data']), f['time'])
    print(len(n['data']), n['time'])
