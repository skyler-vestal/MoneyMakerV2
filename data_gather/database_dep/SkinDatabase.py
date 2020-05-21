import sqlite3 as sql
import SkinScraper
from SkinDef import Skin

class SkinDB:

    def __init__(self, db_path):
        print("Making connection to database")
        self.conn = sql.connect(db_path)
        self.c = self.conn.cursor()
        self.c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='skins' ''')
        if self.c.fetchone()[0] == 1:
            print("Table already exists")
        else:
            print("No table found. Creating new table.")
            self.c.execute("""CREATE TABLE skins (
                collection text,
                type text,
                grade text,
                weapon text,
                skin_name text,
                stat_trak integer,
                price real,
                asset_id text,
                dick_id text,
                market_id text,
                float real
                )""")
            self.conn.commit()

    def __entryExists__(self, skinObj):
        self.c.execute("""SELECT market_id FROM skins WHERE market_id=?""", (skinObj.market_id,))
        data = self.c.fetchall()
        return len(data) != 0
    
    def addSkin(self, skinObj):
        if not self.__entryExists__(skinObj):
            self.c.execute("INSERT INTO skins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (skinObj.collection, skinObj.type, skinObj.grade, skinObj.weapon, skinObj.skin_name, skinObj.stat_trak, skinObj.price,
                skinObj.asset_id, skinObj.dick_id, skinObj.market_id, skinObj.float))
    
    def removeSkin(self, skinObj):
        if self.__entryExists__(skinObj):
            print("Skin being removed: {} | {} ({}) --- (MarketID: {})".format(skinObj.weapon,
                 skinObj.skin_name, skinObj.grade, skinObj.market_id))
            self.c.execute("DELETE FROM skins WHERE market_id=?", (skinObj.market_id,))
        else:
            print("WARNING: Tried to remove {} | {} (MarketID: {}) " +
                "but it's not in the database.")

    def addSkins(self, skinList):
        for skin in skinList:
            self.addSkin(skin)
        self.conn.commit()

    def shaveOldSkins(self, skinList):
        sample = skinList[0]
        self.c.execute("SELECT * FROM skins WHERE weapon=? AND grade=? AND skin_name=? AND stat_trak=?", 
                (sample.weapon, sample.grade, sample.skin_name, sample.stat_trak))
        dbList = self.c.fetchall()
        for dbSkinData in dbList:
            dbSkin = Skin(dbSkinData)
            present = False
            for mSkin in skinList:
                # idk why I have to make them strings for the check to work. Diff encoding?
                if str(mSkin.market_id) == str(dbSkin.market_id):
                    present = True
                    break
            if not present:
                self.removeSkin(dbSkin)
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self, *args):
        print("Saving changes and closing")
        if (len(args) == 0 or (len(args) == 1 and args)):
            self.conn.commit()
        self.conn.close()
        
        



