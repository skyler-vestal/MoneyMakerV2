from sys import path
from os import getcwd
path.insert(0, getcwd() + '\database_dep')

import time

from SkinDatabase import SkinDB
import SkinScraper
from SkinDef import Skin
from SkinPulser import SkinPulse

database_path = 'F:\Dev\py-workspace\SkinDatabase\skins.db'

skinsDB = SkinDB(database_path)
skinP = SkinPulse(41)
try:
    while True:
        skinList = skinP.pulse()
        if skinList is not None:
            for skin in skinList:
                print("Tick #: {} | Skin Data Processed: {}".format(skinP.currTick, skin))
                mSkins = SkinScraper.getMarketList(skin[0], skin[1], skin[2], skin[3])
                skinEntries = [Skin(x) for x in mSkins]
                skinsDB.shaveOldSkins(skinEntries)
                skinsDB.addSkins(skinEntries)
except KeyboardInterrupt:
    print("Closing queries")
    print("NOTE: Tick to resume on in SkinPulse is {}".format(skinP.currTick))
    skinsDB.close()
