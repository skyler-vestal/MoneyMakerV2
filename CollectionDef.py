from SkinDef import Skin

class Collection:

    rarity = ['Consumer', 'Industrial', 'Mil-Spec', 'Restricted', 'Classified', 'Covert']

    def __init__(self, name):
        self.name = name
        self.weapons = ([], [], [], [], [], [])

    def addSkin(self, skin, collection):
        index = 0
        for rar in Collection.rarity:
            if rar in collection:
                self.weapons[index].append(skin.skin_list)
                break
            index += 1
                
