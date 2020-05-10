import requests
from bs4 import BeautifulSoup

file = open("requested_data/skinList.info", "w", encoding='utf-8')
url = 'https://counterstrike.fandom.com/wiki/Skins/List'
request = requests.get(url).text
soup = BeautifulSoup(request, 'lxml')
tables = soup.findAll('table')
table = tables[2]
str = ""
for tr in table.find_all('tr'):
    data = tr.find_all('td')
    data = [i.text.strip() for i in data]
    if len(data) != 0:
        coll = data[0]
        if "Case" in data[0]:
            coll = coll[0:len(coll) - 5]
        str += "{} | {},{}\n".format(data[1], data[2], coll)
file.write(str)