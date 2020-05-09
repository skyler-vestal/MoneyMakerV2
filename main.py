def getSellerPrice(buyer):
    buyer_rd = round(buyer/11.5, 3)
    buyer_rd = buyer_rd - buyer_rd % .01
    deduct = max(.01, buyer_rd)
    buyer_rd = round(buyer/23, 3)
    buyer_rd = buyer_rd - buyer_rd % .01
    deduct += max(.01, buyer_rd)
    seller = round(buyer - deduct, 2)
    return seller
