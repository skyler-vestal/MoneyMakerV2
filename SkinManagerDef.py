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
        self.__initExtra__()

    @staticmethod
    def getSellerPrice(buyer):
        seller = buyer
        buyer_rd = round(buyer/11.5, 3)
        buyer_rd = buyer_rd - buyer_rd % .01
        if buyer_rd < .01:
            seller -= .01
        else:
            seller -= buyer_rd
        buyer_rd = round(buyer/23, 3)
        buyer_rd = buyer_rd - buyer_rd % .01
        if buyer_rd < .01:
            seller -= .01
        else:
            seller -= buyer_rd
        seller = round(seller, 2)
        return seller

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
                stat_trak = skin_entries[0][5] == 'True'
                tmp_skin = Skin(weapon=weapon, skin_name=skin_name, sMin=skin_min, sMax=skin_max)
                for entry in skin_entries:
                    if entry[10] > 0.0:
                        tmp_skin.addSkin(assetID=entry[7], price=entry[10], collection=entry[6])
                tmp_coll = self.__get_coll__(coll_name, stat_trak)
                if tmp_coll == None:
                    tmp_coll = Collection(coll_name, stat_trak)
                    self.collection.append(tmp_coll)
                tmp_coll.addSkin(tmp_skin, skin_type)

    def __initExtra__(self):
        price_file = open("data_gather/requested_data/skinPrice.info", 'r', encoding='utf-8')
        price_lines = price_file.readlines()
        price_lines = [x.strip() for x in price_lines]
        for data_line in price_lines:
            data = data_line.split(',')
            skin_info = data[0].split(" | ")
            weapon = skin_info[0]
            skin_name = skin_info[1]
            tmp_skin = Skin(weapon=weapon, skin_name=skin_name, condition=data[3])
            tmp_skin.addSkin(price=data[5], collection=data[1])
            tmp_coll = self.__get_coll__(data[1], data[4] == 'True')
            if tmp_coll != None:
                tmp_coll.addSkin(tmp_skin, data[2])
        

    def __get_coll__(self, coll_name, stat_trak):
        for coll in self.collection:
            if coll_name == coll.name and stat_trak == coll.stat_trak:
                return coll
        return None


