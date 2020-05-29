class Skin:

    wear_cutoff = [.07, .15, .38, .45, 1.00]
    conditions = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']

    def __init__(self, **kwargs):
        self.weapon = kwargs.get('weapon')
        self.skin_name = kwargs.get('skin_name')
        sMin = kwargs.get('sMin') 
        sMax = kwargs.get('sMax')
        if sMin != None and sMax != None:
            self.sMin = float(sMin)
            self.sMax = float(sMax)
        self.skin_list = ([], [], [], [], [])
        self.real_info = False
    
    def addSkin(self, **kwargs):
        tmp = None
        assetID = kwargs.get('assetID')
        if assetID == None:
            tmp = self.Entity(price=kwargs.get('price'), condition=kwargs.get('collection'))
            index = Skin.__condition_index__(kwargs.get('collection'))
        else:
            self.real_info = True
            tmp = self.Entity(assetID=assetID, sFloat=kwargs.get('sFloat'), price=kwargs.get('price'))
            index = Skin.__wear_index__(kwargs.get('sFloat'))
        tmp.addSkinRef(self)
        self.skin_list[index].append(tmp)
    
    def getEnts(self, float_val):
        return self.skin_list[Skin.__wear_index__(self.getNewfloat(float_val))]

    @staticmethod
    def __wear_index__(val):
        for i in range(len(Skin.wear_cutoff)):
            if (val < Skin.wear_cutoff[i]):
                return i
        return -1

    @staticmethod
    def __condition_index__(val):
        for i in range(len(Skin.conditions)):
            if val == Skin.conditions[i]:
                return i

    def addCollectionRef(self, coll):
        self.collection = coll

    def getNewfloat(self, avgFloat):
        return self.sMin + avgFloat * (self.sMax - self.sMin)

    def getLowestPrice(self):
        lowest = float('inf')
        for ents in self.skin_list:
            for ent in ents:
                if ent.price < lowest:
                    lowest = ent.price
        return lowest

    def __str__(self):
        info = len(self.skin_list) if self.real_info else "-"
        return "{} - {} ({})".format(self.weapon, self.skin_name, info)

    class Entity:
        def __init__(self, **kwargs):
            self.assetID = kwargs.get('assetID')
            if self.assetID == None:
                self.real_info = False
                self.condition = kwargs.get('condition')
                self.sFloat = None
            else:
                self.real_info = True
                self.sFloat = float(kwargs.get('sFloat'))
            tmp_price = kwargs.get('price')
            if isinstance(tmp_price, str):
                tmp_price = float(tmp_price.replace(",", ""))
            self.price = tmp_price
            self.scratch = 0

        def addSkinRef(self, skin):
            self.skin = skin

        def __str__(self):
            if self.real_info:
                return "({} - {})".format(self.price, self.sFloat)
            return "({} - {})".format(self.price, self.condition)