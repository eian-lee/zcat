# index
PRICE, SIZE = range(2)
BID, ASK = 'bids', 'asks'


# 계산함수를 한번만 호출할 경우(함수 1번호출)
def calculate(base, quote):
    return ((float(i[PRICE]) / float(v[PRICE])) for i,v in zip(base[BID], quote[ASK])), ((float(i[PRICE]) / float(v[PRICE])) for i,v in zip(quote[BID], base[ASK]))
