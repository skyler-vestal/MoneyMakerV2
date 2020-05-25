class Skin:

    def __init__(self, **kwargs):
        self.weapon = kwargs.get('weapon')
        self.skin_name = kwargs.get('skin_name')
        self.condition = kwargs.get('condition')
        self.skin_list = []
        if self.condition == None:
            self.sMin = kwargs.get('sMin')
            self.sMax = kwargs.get('sMax')
            self.real_info = True
        else:
            self.real_info = False
    
    def addSkin(self, **kwargs):
        tmp = None
        assetID = kwargs.get('assetID')
        if assetID == None:
            tmp = self.Entity(price=kwargs.get('price'), collection=kwargs.get('collection'))
        else:
            tmp = self.Entity(assetID=assetID, sFloat=kwargs.get('sFloat'), price=kwargs.get('price'))
        self.skin_list.append(tmp)

    def getNewfloat(self, avgFloat):
        return sMin + avgFloat * (sMax - sMin)

    def getLowestPrice(self):
        lowest = float('inf')
        for ent in skin_list:
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
                self.price = kwargs.get('price')
                self.condition = kwargs.get('condition')
                self.scratch = 0
            else:
                self.real_info = True
                self.sFloat = kwargs.get('sFloat')
                self.price = kwargs.get('price')
                self.scratch = 0