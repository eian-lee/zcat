
from itertools import islice
from connector import Connector
from defines import ASK, BID, BITFINEX


class Bitfinex(Connector):
    
    id = BITFINEX
    
    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.format_pairs = f't{self.base.upper()}{self.quote.upper()}'
        self.url = 'wss://api-pub.bitfinex.com/ws/2'
        self.payload = {"event": "subscribe",
                        "channel": "book",
                        "symbol": "tBTCUSD",
                        "prec": "P0",
                        "freq": "F0",
                        "len": 25}
        # 오더북 설정
        self.l2_book = {}
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_pyobj(self.handler(data))
        # self.zsock.send_pyobj(data)
        self.zsock.recv()
        
    def handler(self, message):
        message = message[1]
        # print(message)
        if type(message) is list:
            if len(message) != 3:
                self.l2_book = {'name': self.name,
                                BID: {x[0]: x[-1] for x in message[:25]},
                                ASK: {x[0]: abs(x[-1]) for x in message[25:]}}
                return self.l2_book
            price, count, size = message
            if count != 0:
                side = BID if size > 0 else ASK
                if price in self.l2_book[side]:
                    self.l2_book[side].update({price: abs(size)})
                    return self.l2_book
                self.l2_book[side].update({price: abs(size)})
                self.l2_book[side] = dict(islice(sorted(self.l2_book[side].items()), 25))
                return self.l2_book
            if count == 0:
                side = BID if size == 1 else ASK
                del self.l2_book[side][price]
                return self.l2_book