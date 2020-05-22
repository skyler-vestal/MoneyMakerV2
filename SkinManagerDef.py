import sqlite3 as sql
from SkinDef import Skin
from CollectionDef import Collection

class SkinManager:

    skin_file_path = "data_gather/requested_data/skinRange.info"

    def __init__(self, db_path):
        self.conn = sql.connect(db_path, timeout=10.0)
        self.c = self.conn.cursor()
        self.collection = []
        self.__initData__()

    def __initData__(self):
        print("Initializing database data")
        skin_file = open(SkinManager.skin_file_path, "r", encoding='utf-8')
        skin_list = skin_file.readlines()
        skin_file.close()
        skin_list = [x.strip() for x in skin_list]
        for skin in skin_list:
            skin_data = skin.split(",")
            skin_info = skin_data[0].split(" | ")
            weapon = skin_info[0]
            skin_name = skin_info[1]
            skin_min = skin_data[1]
            skin_max = skin_data[2]
            self.c.execute(''' SELECT * from skins WHERE weapon=? AND skin_name=? ''', (weapon, skin_name))
            skin_entries = self.c.fetchall()
            if (len(skin_entries) > 0):
                print("Adding {} skins".format(skin_data[0]))
                coll_name = skin_entries[0][0]
                skin_type = skin_entries[0][1]
                tmp_skin = Skin(weapon, skin_name, skin_min, skin_max)
                for entry in skin_entries:
                    if entry[10] > 0.0:
                        tmp_skin.addSkin(entry[7], entry[10], entry[6])
                tmp_coll = self.__get_coll__(coll_name)
                if tmp_coll == None:
                    tmp_coll = Collection(coll_name)
                    self.collection.append(tmp_coll)
                tmp_coll.addSkin(tmp_skin, skin_type)

    def __get_coll__(self, name):
        for coll in self.collection:
            if name == coll.name:
                return coll
        return None


