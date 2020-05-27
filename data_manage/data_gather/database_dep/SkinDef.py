class Skin:

    def __init__(self, skinList):
        self.collection = skinList[0]
        self.type = skinList[1]
        self.grade = skinList[2]
        self.weapon = skinList[3]
        self.skin_name = skinList[4]
        self.stat_trak = skinList[5]
        self.price = skinList[6]
        self.asset_id = skinList[7]
        self.dick_id = skinList[8]
        self.market_id = skinList[9]
        self.float = 0

    def __str__(self):
        titleBar = "--------------------"
        res = titleBar + "\n"
        res += "{}: {}\n".format('Collection', self.collection)
        res += "{}: {}\n".format('Type', self.collection)
        res += "{}: {}\n".format('Grade', self.grade)
        res += "{}: {}\n".format('Weapon', self.weapon)
        res += "{}: {}\n".format('Skin Name', self.skin_name)
        res += "{}: {}\n".format('StatTrak', self.stat_trak)
        res += "{}: {}\n".format('Price', self.price)
        res += "{}: {}\n".format('AssetID', self.asset_id)
        res += "{}: {}\n".format('DickID', self.dick_id)
        res += "{}: {}\n".format('MarketID', self.market_id)
        res += "{}: {}\n".format('Float', self.float)
        res += titleBar
        return res

        