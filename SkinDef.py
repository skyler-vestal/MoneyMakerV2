class Skin:

    def __init__(self, weapon, skinName, sMin, sMax):
        self.weapon = weapon
        self.skinName = skinName
        self.sMin = sMin
        self.sMax = sMax
        self.skin_list = []

    def addSkin(self, assetID, sFloat, price):
        tmp = self.Entity(assetID, sFloat, price)
        self.skin_list.append(tmp)

    def getNewfloat(self, avgFloat):
        return sMin + avgFloat * (sMax - sMin)

    class Entity:
        def __init__(self, assetID, sFloat, price):
            self.assetID = assetID
            self.sFloat = sFloat
            self.price = price
            self.scratch = 0