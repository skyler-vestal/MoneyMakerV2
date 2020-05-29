import requests
import time
from bs4 import BeautifulSoup

skin_types = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
skip_words = ['Knife', 'Bayonet', 'Karambit', 'Daggers']
rarity = ['Consumer', 'Industrial', 'Mil-Spec', 'Restricted', 'Classified', 'Covert']
skinRange = []
skinList = []
skinPrice = []

startIndex = 13
endIndex = 1267

rewrite = input("Rewrite file? (y/n): ")
tag = "w" if rewrite == 'y' else 'a'

startSomewhere = input("Custom start index? (nothing if from the start): ")
if startSomewhere != '':
    try:
        startIndex = int(startSomewhere)
    except ValueError:
        print("Input not an integer.")
        exit()
endSomewhere = input("Custom end index? (nothing if at total end): ")
if endSomewhere != '':
    try:
        endIndex = int(endSomewhere)
    except ValueError:
        print("Input not an integer.")
        exit()

skin_file = open("requested_data/skinList.info", tag, encoding='utf-8')
range_file = open("requested_data/skinRange.info", tag, encoding='utf-8')
price_file = open("requested_data/skinPrice.info", tag, encoding='utf-8')
url = 'https://csgostash.com/skin/'

def clean_up():
    closeFile(skin_file, skinList)
    closeFile(range_file, skinRange)
    closeFile(price_file, skinPrice)

def closeFile(info_file, skin_list):
    skin_list.sort()
    printStr = "".join(skin_list)
    printStr = printStr[:len(printStr) - 1]
    info_file.write(printStr)
    info_file.close()

for urlIndex in range(startIndex, endIndex + 1):
    fUrl = url + str(urlIndex)
    try:
        request = requests.get(fUrl).text
    except:
        print("Error detected with retrieving webpage.")
        print("Closing file.")
        clean_up()

    soup = BeautifulSoup(request, 'lxml')
    title = soup.find("div", {"class": "well result-box nomargin"})
    if title == None:
        print("WARNING: Webpage for skin index {} missing. Skipping".format(urlIndex))
        continue
    title = title.text.split('\n')[1]

    collection_data = soup.findAll("p", {"class": "collection-text-label"})
    coll_index = len(collection_data) - 1
    collection = collection_data[coll_index].text if coll_index >= 0 else "Contraband"

    tier = soup.find("p", {"class": "nomargin"})
    tier = tier.text
    for rar in rarity:
        if rar in tier:
            tier = rar
            break

    if any(word in title for word in skip_words):
        print("WARNING: Skin index {} has a skip word (knife?). Skipping".format(urlIndex))
    else:
        print("Processing skin index {} ({})".format(urlIndex, title))
        table_area = soup.findAll("div", {"class": "table-responsive"})[0]
        table = table_area.find("table")
        f_min = soup.findAll("div", {"class": "marker-value cursor-default"})[0].text
        f_max = soup.findAll("div", {"class": "marker-value cursor-default"})[1].text
        skinRange.append("{},{},{}\n".format(title, f_min, f_max))
        for row in table.findAll('tr')[1:]:
            rowData = row.text.split("\n")
            raw_quality = rowData[2]
            if 'Souvenir' not in raw_quality:
                quality = None
                stat_trak = 'StatTrak' in raw_quality
                for q in skin_types:
                    if q in raw_quality:
                        quality = q
                        break
                sellListings = rowData[8]
                if sellListings == '' or '$' in str(sellListings):
                    sellListings = 0
                boughtListings = rowData[14]
                if boughtListings == '' or '$' in str(boughtListings):
                    boughtListings = 0
                skinData = [title, collection, quality, stat_trak, boughtListings, sellListings]
                tmpString = str(title)
                for pt in skinData[1:]:
                    tmpString += ',' + str(pt)
                skinList.append(tmpString + '\n')
                priceListings = rowData[5]
                if int(boughtListings) < 50 and priceListings != '' and '$' in str(priceListings):
                    price = priceListings.replace('$', '')
                    price = price.replace(',', '')
                    priceData = [title, collection, tier, quality, stat_trak, price, f_min, f_max]
                    tmpString = str(title)
                    for pt in priceData[1:]:
                        tmpString += ',' + str(pt)
                    skinPrice.append(tmpString + '\n')
print("Success! Writing to file.")
clean_up()

