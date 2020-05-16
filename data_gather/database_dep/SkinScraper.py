import urllib.error as err
import urllib.request as req
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
from time import sleep

cooldown_time = 120

rarity = ['Consumer Grade', 'Industrial Grade', 'Mil-Spec', 'Restricted', 'Classified', 'Covert']
stemUrl = 'https://steamcommunity.com/market/listings/730/'
query = '/render?start=0&count={}&currency=1&language=english&format=json'

def __check_request__(url):
    mPage = None
    try:
        mPage = req.urlopen(url)
    except err.HTTPError as e:
        print("WARNING: " + str(e) + ": " + url)
        mPage = None
    except:
        print("WARNING: Unexpected error (timeout?): " + url)
        mPage = None
    return mPage

def getMarketList(skinName, skinType, statTrak, reqNum):
    statName = "StatTrak%E2%84%A2%20" if statTrak == "True" else ""
    fullSkinName = statName + quote(skinName) + " (" + skinType + ")"
    reqUrl = stemUrl + fullSkinName + query.format(reqNum)
    reqUrl = reqUrl.replace(' ', '%20')
    mPage = __check_request__(reqUrl)
    while mPage is None:
        print("Requested page pulled up as none. Waiting {} seconds".format(cooldown_time))
        sleep(cooldown_time)
        mPage = __check_request__(reqUrl)
    return __scrapeMarketPage__(mPage, skinName, skinType, statTrak) if mPage is not None else None

def __scrapeMarketPage__(mPage, skinName, skinType, statTrak):
    returnList = []
    data = json.loads(mPage.read().decode())
    soup = BeautifulSoup(data['results_html'], 'lxml')
    prices_html = soup.find_all('span', {"class": "market_listing_price market_listing_price_with_fee"})
    prices = [i.text.strip()[1:] for i in prices_html]
    skinSplit = skinName.split(" | ")
    weapon = skinSplit[0]
    weaponSkin = skinSplit[1]
    collection = ""
    rarityType = ""
    listings = data['listinginfo']
    if len(listings) > 0:
        index = 0
        for skin in listings.items():
            info = skin[1]
            listingid = info['listingid']
            asset = info['asset']
            assetid = asset['id']
            assetDetails = data['assets']['730']['2'][str(assetid)]
            if rarityType == "":
                for rar in rarity:
                    if rar in assetDetails['type']:
                        rarityType = rar
                        break
            if collection == "":
                collection = assetDetails['descriptions'][4]['value']
            inspUrl = asset['market_actions'][0]['link']
            startIndex = inspUrl.index('D') + 1
            dickid = inspUrl[startIndex:]
            skin = (collection, skinType, weapon, weaponSkin, statTrak, prices[index], assetid, dickid, listingid)
            returnList.append(skin)
            index += 1
    return returnList
