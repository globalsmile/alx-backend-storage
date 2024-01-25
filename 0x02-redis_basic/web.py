#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import requests
import time
import redis
r = redis.Redis()


def get_page(url: str) -> str:
    """ track how many times a particular URL was accessed in the key
        "count:{url}"
        and cache the result with an expiration time of 10 seconds """
    if r.get(f'count:{url}'):
        r.incr(f'count:{url}')
        return r.get(f'count:{url}')
    else:
        r.set(f'count:{url}', 1)
        r.expire(f'count:{url}', 10)
        return requests.get(url).text

if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    get_page(url)

    

