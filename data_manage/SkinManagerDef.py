import sqlite3 as sql
from data_manage.SkinDef import Skin
from data_manage.CollectionDef import Collection

class SkinManager:

    skin_file_path = "data_manage/data_gather/requested_data/skinRange.info"
    skin_price_path = "data_manage/data_gather/requested_data/skinPrice.info"

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
        skin_list = SkinManager.__get_lines__(SkinManager.skin_file_path)
        for skin in skin_list:
            skin_data = skin.split(",")
            weapon, skin_name = SkinManager.__parse_head__(skin_data[0])
            skin_min = skin_data[1]
            skin_max = skin_data[2]
            self.c.execute(''' SELECT * from skins WHERE weapon=? AND skin_name=? ''', (weapon, skin_name))
            skin_entries = self.c.fetchall()
            if (len(skin_entries) > 0):
                print("Adding {} skins".format(skin_data[0]))
                coll_name = skin_entries[0][0]
                skin_type = skin_entries[0][1]
                tmp_skin = Skin(weapon=weapon, skin_name=skin_name, sMin=skin_min, sMax=skin_max)
                tmp_skin_stat = Skin(weapon=weapon, skin_name=skin_name, sMin=skin_min, sMax=skin_max)
                for entry in skin_entries:
                    if entry[10] > 0.0 and entry[6] != 'old!':
                        if entry[5] == 'True':
                            tmp_skin_stat.addSkin(assetID=entry[7], price=entry[6], sFloat=entry[10])
                        else:
                            tmp_skin.addSkin(assetID=entry[7], price=entry[6], sFloat=entry[10])
                self.__add_coll__(coll_name, True, tmp_skin_stat, skin_type)
                self.__add_coll__(coll_name, False, tmp_skin, skin_type)

    def __initExtra__(self):
        price_lines = SkinManager.__get_lines__(SkinManager.skin_price_path)
        for data_line in price_lines:
            data = data_line.split(',')
            weapon, skin_name = SkinManager.__parse_head__(data[0])
            tmp_skin = Skin(weapon=weapon, skin_name=skin_name)
            tmp_skin.addSkin(price=data[5], collection=data[3])
            tmp_coll = self.__get_coll__(data[1], data[4] == 'True')
            if tmp_coll != None:
                in_coll = False
                for wepList in tmp_coll.weapons:
                    if in_coll:
                        break
                    for skin in wepList:
                        if skin.weapon == weapon and skin.skin_name == skin_name:
                            in_coll = True
                            skin.addSkin(price=data[5], collection=data[3])
                if not in_coll:
                    tmp_coll.addSkin(tmp_skin, data[2])

    def __add_coll__(self, coll_name, stat_trak, skins, skin_type):
        if len(skins.skin_list) > 0:
            tmp_coll = self.__get_coll__(coll_name, stat_trak)
            if tmp_coll == None:
                tmp_coll = Collection(coll_name, stat_trak)
                self.collection.append(tmp_coll)
            tmp_coll.addSkin(skins, skin_type)
        
    def __get_coll__(self, coll_name, stat_trak):
        for coll in self.collection:
            if coll_name == coll.name and stat_trak == coll.stat_trak:
                return coll
        return None

    @staticmethod 
    def __get_lines__(file_path):
        tmp_file = open(file_path, 'r', encoding='utf-8')
        tmp_lines = tmp_file.readlines()
        tmp_file.close()
        tmp_lines = [x.strip() for x in tmp_lines]
        return tmp_lines

    @staticmethod
    def __parse_head__(weapon_str):
        skin_info = weapon_str.split(" | ")
        weapon = skin_info[0]
        skin_name = skin_info[1]
        return weapon, skin_name


