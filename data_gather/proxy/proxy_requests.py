import requests
from urllib import request as urlrequest
import random


class ProxyRequests:

    def __init__(self):
        f = open("proxy/proxy_list.info")
        self.proxies = f.readlines()
        f.close()
        self.proxies = [x.strip() for x in self.proxies]

    def get_random_proxy(self):
        try:
            return random.choice(self.proxies)
        except IndexError:
            return None

    def remove_proxy(self, proxy):
        try:
            self.proxies.remove(proxy)
        except ValueError:
            pass

    def get(self, url):
        """Calls requests.get using a proxy from the list"""
        while len(self.proxies) > 0:
            cur_proxy = self.get_random_proxy()
            print('Trying proxy {}, {} proxies left.'.format(cur_proxy, len(self.proxies)))
            proxies = {
                'http': cur_proxy,
                'https': cur_proxy
            }
            req = urlrequest.Request(url)
            req.set_proxy(cur_proxy, 'http')
            res = urlrequest.urlopen(req)
            return res
        print('Proxy list empty!')
        return None


if __name__ == '__main__':
    proxy_requests = ProxyRequests()
    print(len(proxy_requests.proxies))
    result = proxy_requests.get('https://www.google.com')
    print(result.text)
    print(len(proxy_requests.proxies))
