import urllib.request as req
import json

stemUrl = 'https://steamcommunity.com/market/listings/730/'
url = 'AWP | Asiimov (Field-Tested)'
query = '/render?start=0&count=1&currency=1&language=english&format=json'
fUrl = stemUrl + url + query
fUrl = fUrl.replace(' ', '%20')
with req.urlopen(fUrl) as url:
    data = json.loads(url.read().decode())
    meme = data.dumps
    print(data)
