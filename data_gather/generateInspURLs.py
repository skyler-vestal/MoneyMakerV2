import json
from bs4 import BeautifulSoup
import time

import os
from sys import path
path.insert(0, os.getcwd() + '/proxy')
from proxy_requests import ProxyRequests

requestAmount = 20

skinTypes = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
f = open("requested_data/skinList.info", encoding='utf8')
skinList = f.read().splitlines()

pReq = ProxyRequests()
base_headers = {
    'Accept-Language': 'en-US',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
}


def check_request(url):
    mPage = None
    mPage = pReq.get(reqUrl)
    if mPage is None:
        print('Uh oh')
    return mPage

stemUrl = 'https://steamcommunity.com/market/listings/730/'
query = '/render?start=0&count={}&currency=1&language=english&format=json'.format(requestAmount)
formatList = []
for skinName in skinList:
    for skinType in skinTypes:
        fullSkinName = skinName + " (" + skinType + ")"
        reqUrl = stemUrl + fullSkinName + query
        reqUrl = reqUrl.replace(' ', '%20')
        print("Writing data for " + fullSkinName)
        mPage = check_request(reqUrl)
        while mPage is None:
            time.sleep(1)
            mPage = check_request(reqUrl)
        data = json.loads(mPage.read().decode())
        soup = BeautifulSoup(data['results_html'], 'lxml')
        prices_html = soup.find_all('span', {"class": "market_listing_price market_listing_price_with_fee"})
        prices = [i.text.strip() for i in prices_html]
        collection = ""
        listings = data['listinginfo']
        if len(listings) > 0:
            index = 0
            for skin in listings.items():
                info = skin[1]
                listingid = info['listingid']
                asset = info['asset']
                assetid = asset['id']
                if collection == "":
                    collection = data['assets']['730']['2'][str(assetid)]['descriptions'][4]['value']
                inspUrl = asset['market_actions'][0]['link']
                startIndex = inspUrl.index('D') + 1
                dickid = inspUrl[startIndex:]
                formatString = "{},{},{},{},{},{}\n".format(fullSkinName, collection, prices[index], assetid, dickid, listingid)
                formatList.append(formatString)
                index += 1
write_string = "".join(formatList)
writeFile = open("requested_data/skinData.info", "w")
writeFile.write(write_string[:len(write_string) - 1])
writeFile.close()
