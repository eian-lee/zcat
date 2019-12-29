from defines import ASK, BID, PRICE, SIZE

def calculate(base, quote):
    return ((float(i) / float(v)) for i,v in zip(base[BID], quote[ASK])), ((float(i) / float(v)) for i,v in zip(quote[BID], base[ASK]))

def update_asks_bids(ad, bd):
    """크라켄 ASK & BID 아래처럼 병렬처리하여 반환
    >>> [(ASK가격, ASK수량) ... ] , [(BID가격, BID수량) ... ]
    """
    return ((x[0], x[1]) for k,v in ad.items() for i,x in enumerate(v)), ((x[0], x[1]) for k,v in bd.items() for i,x in enumerate(v))
    