from data_manage.SkinDef import Skin

class Collection:

    rarity = ['Consumer', 'Industrial', 'Mil-Spec', 'Restricted', 'Classified', 'Covert']

    def __init__(self, name, stat_trak):
        self.name = name
        self.weapons = ([], [], [], [], [], [])
        self.stat_trak = stat_trak

    def addSkin(self, skin, ware):
        index = 0
        for rar in Collection.rarity:
            if rar in ware:
                self.weapons[index].append(skin)
                break
            index += 1

    def __str__(self):
        append = "*" if self.stat_trak else ""
        return self.name + append
                
