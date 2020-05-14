import requests
import time
from bs4 import BeautifulSoup

skin_types = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
skip_words = ['Knife', 'Bayonet', 'Karambit', 'Daggers']
skinList = []
skinRange = []

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
url = 'https://csgostash.com/skin/'

def closeFile():
    skinList.sort()
    skinRange.sort()
    printStr = "".join(skinList)
    printStr = printStr[:len(printStr) - 1]
    skin_file.write(printStr)
    skin_file.close()
    printStr = "".join(skinRange)
    printStr = printStr[:len(printStr) - 1]
    range_file.write(printStr)
    range_file.close()

for urlIndex in range(startIndex, endIndex + 1):
    fUrl = url + str(urlIndex)
    try:
        request = requests.get(fUrl).text
    except:
        print("Error detected with retrieving webpage.")
        print("Closing file.")
        closeFile()

    soup = BeautifulSoup(request, 'lxml')
    title = soup.findAll("div", {"class": "well result-box nomargin"})
    if len(title) == 0:
        print("WARNING: Webpage for skin index {} missing. Skipping".format(urlIndex))
        continue
    title = title[0].text.split('\n')[1]

    if any(word in title for word in skip_words):
        print("WARNING: Skin index {} has a skip word (knife?). Skipping".format(urlIndex))
    else:
        print("Processing skin index {} ({})".format(urlIndex, title))
        table_area = soup.findAll("div", {"class": "table-responsive"})[0]
        table = table_area.find("table")
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
                skinData = [title, quality, stat_trak, boughtListings, sellListings]
                tmpString = str(title)
                for pt in skinData[1:]:
                    tmpString += ',' + str(pt)
                skinList.append(tmpString + '\n')
        min = soup.findAll("div", {"class": "marker-value cursor-default"})[0].text
        max = soup.findAll("div", {"class": "marker-value cursor-default"})[1].text
        skinRange.append("{},{},{}\n".format(title, min, max))
print("Success! Writing to file.")
closeFile()

