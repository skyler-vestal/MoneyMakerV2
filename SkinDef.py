class Skin:

    def __init__(self, **kwargs):
        self.weapon = kwargs.get('weapon')
        self.skin_name = kwargs.get('skin_name')
        self.sMin = kwargs.get('sMin')
        self.sMax = kwargs.get('sMax')
        self.skin_list = []
        self.real_info = False
    
    def addSkin(self, **kwargs):
        tmp = None
        assetID = kwargs.get('assetID')
        if assetID == None:
            tmp = self.Entity(price=kwargs.get('price'), collection=kwargs.get('collection'))
        else:
            self.real_info = True
            tmp = self.Entity(assetID=assetID, sFloat=kwargs.get('sFloat'), price=kwargs.get('price'))
        self.skin_list.append(tmp)

    def getNewfloat(self, avgFloat):
        return sMin + avgFloat * (sMax - sMin)

    def getLowestPrice(self):
        lowest = float('inf')
        for ent in self.skin_list:
            if ent.price < lowest:
                lowest = ent.price
        return lowest

    def __repr__(self):
        info = len(self.skin_list) if self.real_info else "-"
        return "{} - {} ({})".format(self.weapon, self.skin_name, info)

    class Entity:
        def __init__(self, **kwargs):
            self.assetID = kwargs.get('assetID')
            if self.assetID == None:
                self.real_info = False
                self.condition = kwargs.get('condition')
            else:
                self.real_info = True
                self.sFloat = float(kwargs.get('sFloat'))
            tmp_price = kwargs.get('price')
            if isinstance(tmp_price, str):
                tmp_price = float(tmp_price.replace(",", ""))
            self.price = tmp_price
            self.scratch = 0