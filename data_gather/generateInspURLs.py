from sys import path
from os import getcwd
path.insert(0, getcwd() + '/database_dep')

import SkinScraper
from SkinDef import Skin

skinTypes = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
f = open("requested_data/skinList.info", encoding='utf8')
skinList = f.read().splitlines()

meme = Skin(SkinScraper.getMarketList('AK-47 | Aquamarine Revenge', 'Factory New', False)[0])
print(meme)


