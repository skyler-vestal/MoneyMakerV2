class Skin:

    def __init__(self, skinList):
        self.collection = skinList[0]
        self.grade = skinList[1]
        self.weapon = skinList[2]
        self.skinName = skinList[3]
        self.statTrak = skinList[4]
        self.price = skinList[5]
        self.assetID = skinList[6]
        self.dickID = skinList[7]
        self.marketID = skinList[8]

    def __str__(self):
        titleBar = "--------------------"
        res = titleBar + "\n"
        res += "{}: {}\n".format('Collection', self.collection)
        res += "{}: {}\n".format('Grade', self.grade)
        res += "{}: {}\n".format('Weapon', self.weapon)
        res += "{}: {}\n".format('SkinName', self.skinName)
        res += "{}: {}\n".format('StatTrak', self.statTrak)
        res += "{}: {}\n".format('Price', self.price)
        res += "{}: {}\n".format('AssetID', self.assetID)
        res += "{}: {}\n".format('DickID', self.dickID)
        res += "{}: {}\n".format('MarketID', self.marketID)
        res += titleBar
        return res

        