from sys import path
from os import getcwd
path.insert(0, getcwd() + '\database_dep')

from SkinDatabase import SkinDB
import SkinScraper
from SkinDef import Skin

database_path = 'F:\Dev\py-workspace\SkinDatabase\skins.db'

skinTypes = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
f = open("requested_data/skinList.info", encoding='utf8')
skinList = f.read().splitlines()

skins = SkinDB(database_path)
index = 0
for skin in skinList:
    for skinType in skinTypes:
        mSkins = SkinScraper.getMarketList(skin, skinType, False)
        skins.addSkins([Skin(x) for x in mSkins])
    index += 1
    if index > 3:
        break
skins.close()
