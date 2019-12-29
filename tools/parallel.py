from defines import ASK, BID, PRICE, SIZE

def calculate(base, quote):
    return ((float(i) / float(v)) for i,v in zip(base[BID], quote[ASK])), ((float(i) / float(v)) for i,v in zip(quote[BID], base[ASK]))

def update_asks_bids(ad, bd):
    """ 크라켄은 수신된 가격리스트의 길이 제한이 없음
        웹소켓으로 가격정보가 수신되고
        그 다음 가격정보가 수신될 때 까지 시간을 측정하면,
        변동이 적당한 경우 10만분의 1초부터
        변동이 심하면 100만분의 1초에 육박함
        
        XXX: 가격 리스트를 순회하다 다음 가격리스트가 수신될 수 있으므로
        크라켄만 이렇게 가독성을 버리고,
        Parallel Assignment를 통해
        튜플컴프리헨션, items, enumerate를 중첩사용
        ZeroMQ 이외 비동기 라이브러리로 처리가 불가능한걸로 판단됨
        C로 마이그레이션 또는 PyPy 사용권장
        
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
    