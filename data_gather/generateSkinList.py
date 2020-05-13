import requests
from bs4 import BeautifulSoup

file = open("requested_data/skinList.info", "w", encoding='utf-8')
url = 'https://counterstrike.fandom.com/wiki/Skins/List'
request = requests.get(url).text
soup = BeautifulSoup(request, 'lxml')
tables = soup.findAll('table')
skinList = []
for table in tables:
    for tr in table.find_all('tr'):
        data = tr.find_all('td')
        data = [i.text.strip() for i in data]
        if len(data) != 0:
            skinList.append("{} | {}\n".format(data[1], data[2]))
skinList.sort()
str = ""
for skin in skinList:
    str += skin
str = str[:len(str) - 1]
file.write(str)