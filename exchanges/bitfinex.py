
from itertools import islice
from connector import Connector
from defines import ASK, BID, BITFINEX


class Bitfinex(Connector):
    
    id = BITFINEX
    
    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.format_pairs = "t{}{}".format(self.base.upper(), self.quote.upper())
        self.url = 'wss://api-pub.bitfinex.com/ws/2'
        self.payload = {"event": "subscribe",
                        "channel": "book",
                        "symbol": "tBTCUSD",
                        "prec": "P0",
                        "freq": "F0",
                        "len": 25}
        # 오더북 설정
        self._book = {}
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_json(self.handler(data))
        self.zsock.recv()
        
    def handler(self, message):
        message = message[1]
        if type(message) is list:
            # 스냅샷 저장
            if len(message) != 3:
                self._book = {'name': self.name,
                              'bids': {x[0]: x[-1] for x in message[:25]},
                              'asks': {x[0]: abs(x[-1]) for x in message[25:]}}
                return self._book
            # 메시지 언패킹
            price, count, size = message
            # 카운트가 0이 아닌경우
            if count != 0:
                # 주문판단
                side = BID if size > 0 else ASK
                # 업데이트된 가격 내 오더북에 있는경우
                if price in self._book[side]:
                    # 내 오더북의 주문을 갱신
                    self._book[side].update({price: abs(size)})
                    return self._book
                # 업데이트된 가격이 내 오더북에 없는 경우 삽입
                self._book[side].update({price: abs(size)})
                # 정렬 후 딕셔너리 슬라이싱으로 깊이 유지
                self._book[side] = dict(islice(sorted(self._book[side].items()), 25))
                return self._book
            # 카운트가 0인 경우
            if count == 0:
                # 사이즈가 1이면 BID 삭제, 다른경우 ASK 삭제
                side = BID if size == 1 else ASK
                del self._book[side][price]
                return self._book