from defines import ASK, BID, PRICE, SIZE
from timer import timer

# @timer
def calculate(base, quote):
    return [(float(i) / float(v)) for i,v in zip(base[BID], quote[ASK])], [(float(i) / float(v)) for i,v in zip(quote[BID], base[ASK])]

def update_asks_bids(ad, bd):
    """ 크라켄은 가격리스트가 여러개 수신됨
        가격리스트가 수신되고 나서
        다음 가격리스트가 수신될 때까지 시간은,
        10만분의 1초 ~ 100만분의 1초(변동에 따라)
        
        XXX: 가격리스트를 탐색중 다음 가격리스트가 누락방지를 위해
        크라켄은 가독성을 포기하고 Parallel Assignment,
        튜플컴프리헨션, items, enumerate를 중첩사용
        
        ZeroMQ 이외 비동기모듈은 매우 불리함
        C로 마이그레이션하거나 PyPy도 좋은선택이다
        
    >>> [
            (ASK가격1, ASK수량1),
            (ASK가격2, ASK수량2),
            (ASK가격3, ASK수량3),
            ... ),
        ],
        [
            (BID가격1, BID수량1),
            (BID가격2, BID수량2),
            (BID가격3, BID수량3),
            ... ),
        ]
    """
    return ((x[0], x[1]) for k,v in ad.items() for i,x in enumerate(v)), ((x[0], x[1]) for k,v in bd.items() for i,x in enumerate(v))